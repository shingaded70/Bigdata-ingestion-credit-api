# API Endpoints Documentation

Base URL example (local):
- `http://localhost:8000`

All data endpoints require an **API key** in the header:
- `X-API-Key: demo-api-key-123`

---

## 1. GET /data/transactions

Returns a paginated list of transactions with optional filters.

**URL:**
- `/data/transactions`

**Method:**
- `GET`

**Headers:**
- `X-API-Key: <your-api-key>`

**Query Parameters:**

- `start_date` (optional, string, format: `YYYY-MM-DD`)
- `end_date` (optional, string, format: `YYYY-MM-DD`)
- `country` (optional, string, example: `IN`, `US`)
- `page` (optional, integer, default: `1`)
- `page_size` (optional, integer, default: `100`, max: `1000`)

**Sample Request:**

```http
GET /data/transactions?start_date=2025-11-01&end_date=2025-11-02&country=IN&page=1&page_size=100
X-API-Key: demo-api-key-123
```

**Sample Response:**

```json
{
  "data": [
    {
      "transaction_id": "txn_1732342342342",
      "user_id": "user_42",
      "timestamp": "2025-11-01T12:34:56",
      "amount": 123.45,
      "currency": "USD",
      "category": "shopping",
      "country": "IN"
    }
  ],
  "page": 1,
  "page_size": 100,
  "records_returned": 1,
      "credits_consumed": 1
}
```

---

## 2. GET /me/credits

Returns the remaining credits for the current API key.

**URL:**
- `/me/credits`

**Method:**
- `GET`

**Headers:**
- `X-API-Key: <your-api-key>`

**Sample Response:**

```json
{
  "user_id": 1,
  "name": "Demo User",
  "credits_remaining": 995
}
```

---
