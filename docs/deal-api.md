# Deal API Documentation

The Deal API provides endpoints for managing trading deals within the Horizon Router system.

## Base URL

All endpoints are prefixed with the API base URL.

## Endpoints

### 1. Create Deal

**POST** `/deals/`

Creates a new trading deal record.

**Request Body:**

```json
{
  "token": "string", // Required, max 255 chars
  "strategy_prefix": "STR", // Required, max 50 chars
  "strategy_name": "Strategy Name", // Required, max 255 chars
  "time": "2023-10-01T10:00:00Z", // Required, ISO 8601 format
  "symbol": "EURUSD", // Required, max 100 chars
  "type": 0, // Required, integer (0 = ORDER_TYPE_BUY, 1 = ORDER_TYPE_SELL)
  "direction": 0, // Required, integer (0 = IN, 1 = OUT)
  "volume": 0.1, // Required, number
  "price": 1.085, // Required, number
  "profit": 10.5, // Optional, number
  "take_profit_price": 1.09, // Optional, number
  "stop_loss_price": 1.08, // Optional, number
  "broker_account_number": "123456" // Required, string, max 255 chars
}
```

**Response:**

**201 Created:**

```json
{
  "success": true,
  "message": "Deal created successfully",
  "data": {
    "id": 1
  }
}
```

**400 Bad Request:**

```json
{
  "success": false,
  "code": 400,
  "message": "Validation failed",
  "error": {
    "field_name": ["error details"]
  }
}
```

**404 Not Found:**

```json
{
  "success": false,
  "code": 404,
  "message": "Strategy with prefix 'STR' and name 'Strategy Name' does not exist"
}
```

### 2. Search Deals

**GET** `/deals/`

Retrieves deals with optional filtering.

**Query Parameters:**

- `id` (optional): Filter by deal ID. If not provided, returns all deals.

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Deals retrieved successfully",
  "data": [
    {
      "id": 1,
      "token": "string",
      "strategy": {
        "id": 123,
        "name": "Strategy Name",
        "prefix": "STR"
      },
      "time": "2023-10-01T10:00:00Z",
      "symbol": "EURUSD",
      "type": 0,
      "direction": 0,
      "volume": "0.1",
      "price": "1.0850",
      "profit": "10.50",
      "take_profit_price": "1.0900",
      "stop_loss_price": "1.0800",
      "account": {
        "id": 456,
        "name": "Account Name"
      },
      "created_at": "2023-10-01T10:00:00Z",
      "updated_at": "2023-10-01T10:00:00Z"
    }
  ]
}
```

### 3. Update Deal

**PUT** `/deals/{deal_id}/`

Updates an existing deal. All fields are optional.

**Path Parameters:**

- `deal_id`: ID of the deal to update

**Request Body:**

```json
{
  "token": "string", // Optional, max 255 chars
  "strategy_prefix": "STR", // Optional, max 50 chars
  "strategy_name": "Strategy Name", // Optional, max 255 chars
  "time": "2023-10-01T10:00:00Z", // Optional, ISO 8601 format
  "symbol": "EURUSD", // Optional, max 100 chars
  "type": 0, // Optional, integer (0 = ORDER_TYPE_BUY, 1 = ORDER_TYPE_SELL)
  "direction": 0, // Optional, integer (0 = IN, 1 = OUT)
  "volume": 0.1, // Optional, number
  "price": 1.085, // Optional, number
  "profit": 10.5, // Optional, number
  "take_profit_price": 1.09, // Optional, number
  "stop_loss_price": 1.08, // Optional, number
  "broker_account_number": "123456" // Optional, string, max 255 chars
}
```

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Deal updated successfully"
}
```

**400 Bad Request:**

```json
{
  "success": false,
  "code": 400,
  "message": "Validation failed",
  "error": {
    "field_name": ["error details"]
  }
}
```

**404 Not Found:**

```json
{
  "success": false,
  "code": 404,
  "message": "Deal with id 123 does not exist"
}
```

### 4. Delete Deal

**DELETE** `/deals/{deal_id}/`

Deletes a deal by ID.

**Path Parameters:**

- `deal_id`: ID of the deal to delete

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Deal deleted successfully"
}
```

**404 Not Found:**

```json
{
  "success": false,
  "code": 404,
  "message": "Deal with id 123 does not exist"
}
```

## Data Types

### Type Values (DealTypes)

- `0`: ORDER_TYPE_BUY
- `1`: ORDER_TYPE_SELL

### Direction Values (DealDirections)

- `0`: IN
- `1`: OUT

### Time Format

All timestamps use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

## Response Format

All API responses follow a consistent format based on the status code:

### Success Responses (2xx)

```json
{
  "success": true,
  "message": "Descriptive success message",
  "data": {} // Optional response data
}
```

### Error Responses (4xx/5xx)

```json
{
  "success": false,
  "code": 400, // HTTP status code
  "message": "Descriptive error message",
  "error": {} // Optional error details (e.g., validation errors)
}
```

### Common Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request format or validation errors
- **404 Not Found**: Requested resource not found
- **500 Internal Server Error**: Server error
