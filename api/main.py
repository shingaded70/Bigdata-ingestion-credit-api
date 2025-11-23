# FastAPI app exposing a credit-regulated data API.
#
# Note: For assignment/demo purposes, this implementation uses in-memory
# dummy data for users and credits instead of a real database.

from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

from clickhouse_driver import Client as CHClient
from .credit_logic import calculate_credits, has_sufficient_credits

app = FastAPI(
    title="Big Data Credit-Based API",
    description="Example FastAPI application for a credit-regulated data API.",
    version="1.0.0"
)

# Dummy users stored in memory (would normally be in PostgreSQL)
DUMMY_USERS = {
    "demo-api-key-123": {
        "user_id": 1,
        "name": "Demo User",
        "credits_remaining": 1000
    }
}

# Example ClickHouse client (adjust host/database as needed)
ch_client = CHClient(host="localhost", database="analytics")


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    timestamp: datetime
    amount: float
    currency: str
    category: str
    country: str


class TransactionsResponse(BaseModel):
    data: List[Transaction]
    page: int
    page_size: int
    records_returned: int
    credits_consumed: int


def get_user_from_api_key(api_key: str) -> Dict[str, Any]:
    user = DUMMY_USERS.get(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user


@app.get("/data/transactions", response_model=TransactionsResponse)
def get_transactions(
    api_key: str = Header(..., alias="X-API-Key"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    country: Optional[str] = Query(None, description="Country code filter"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000)
):
    user = get_user_from_api_key(api_key)

    filters = []
    if start_date:
        filters.append(f"timestamp >= toDateTime('{start_date} 00:00:00')")
    if end_date:
        filters.append(f"timestamp <= toDateTime('{end_date} 23:59:59')")
    if country:
        filters.append(f"country = '{country}'")

    where_clause = " AND ".join(filters)
    if where_clause:
        where_clause = "WHERE " + where_clause

    offset = (page - 1) * page_size
    query = f"""
        SELECT
            transaction_id,
            user_id,
            timestamp,
            amount,
            currency,
            category,
            country
        FROM transactions
        {where_clause}
        ORDER BY timestamp
        LIMIT {page_size} OFFSET {offset}
    """

    rows = ch_client.execute(query)
    records_returned = len(rows)

    credits_to_charge = calculate_credits(records_returned)

    if not has_sufficient_credits(user["credits_remaining"], credits_to_charge):
        raise HTTPException(status_code=402, detail="Insufficient credits")

    # Deduct credits (for demo we mutate in memory)
    user["credits_remaining"] -= credits_to_charge

    data = [
        Transaction(
            transaction_id=r[0],
            user_id=r[1],
            timestamp=r[2],
            amount=float(r[3]),
            currency=r[4],
            category=r[5],
            country=r[6]
        )
        for r in rows
    ]

    return TransactionsResponse(
        data=data,
        page=page,
        page_size=page_size,
        records_returned=records_returned,
        credits_consumed=credits_to_charge
    )


@app.get("/me/credits")
def get_my_credits(api_key: str = Header(..., alias="X-API-Key")):
    user = get_user_from_api_key(api_key)
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "credits_remaining": user["credits_remaining"]
    }
