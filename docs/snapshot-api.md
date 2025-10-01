# Snapshot API Documentation

The Snapshot API provides endpoints for managing account and strategy snapshots within the Horizon Router system. Snapshots capture the state of accounts and strategies at specific events, including NAV (Net Asset Value) and exposure information.

## Base URL

All endpoints are prefixed with the API base URL.

## Endpoints

### 1. Create Snapshot

**POST** `/snapshot/`

Creates a new snapshot record for an account and optionally associates it with a strategy.

**Request Body:**

```json
{
  "broker_account_number": "MT5-123456", // Required, string, max 255 chars, cannot be empty
  "strategy_prefix": "GBPUSD_M15", // Optional, string, max 50 chars, cannot be empty, nullable
  "event": "Position opened", // Required, string, max 255 chars, cannot be empty
  "nav": "10000.50", // Required, string, decimal format
  "exposure": "2500.75" // Required, string, decimal format
}
```

**Response:**

**201 Created:**

```json
{
  "success": true,
  "message": "Snapshot created successfully",
  "data": {
    "id": 123
  }
}
```

**400 Bad Request (Invalid JSON):**

```json
{
  "success": false,
  "code": 400,
  "message": "Invalid JSON format"
}
```

**400 Bad Request (Validation Failed):**

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

**400 Bad Request (Invalid Decimal):**

```json
{
  "success": false,
  "code": 400,
  "message": "Invalid decimal format for nav or exposure"
}
```

**404 Not Found (Account):**

```json
{
  "success": false,
  "code": 404,
  "message": "Account with broker_account_number MT5-123456 does not exist"
}
```

**404 Not Found (Strategy):**

```json
{
  "success": false,
  "code": 404,
  "message": "Strategy with prefix GBPUSD_M15 does not exist"
}
```

### 2. Search Snapshots

**GET** `/snapshot/search/`

Retrieves snapshots with optional filtering by account, strategy, or event.

**Query Parameters:**

- `broker_account_number` (optional): Filter by account's broker account number
- `strategy_prefix` (optional): Filter by strategy prefix
- `event` (optional): Filter by event description (partial match, case-insensitive)

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Snapshots retrieved successfully",
  "data": [
    {
      "id": 123,
      "account": {
        "id": 1,
        "broker_account_number": "MT5-123456",
        "name": "Main Account"
      },
      "strategy": {
        "id": 5,
        "prefix": "GBPUSD_M15",
        "name": "GBP/USD M15 Strategy"
      },
      "event": "Position opened",
      "nav": "10000.50",
      "exposure": "2500.75",
      "created_at": "2025-10-01T10:30:00Z",
      "updated_at": "2025-10-01T10:30:00Z"
    }
  ]
}
```

### 3. Update Snapshot

**PUT** `/snapshot/{snapshot_id}/`

Updates an existing snapshot record. All fields are optional - only provided fields will be updated.

**Request Body:**

```json
{
  "broker_account_number": "MT5-789012", // Optional, string, max 255 chars, cannot be empty
  "strategy_prefix": "EURUSD_M30", // Optional, string, max 50 chars, cannot be empty, nullable
  "event": "Position modified", // Optional, string, max 255 chars, cannot be empty
  "nav": "11500.25", // Optional, string, decimal format
  "exposure": "3000.00" // Optional, string, decimal format
}
```

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Snapshot updated successfully"
}
```

**400 Bad Request (Invalid JSON):**

```json
{
  "success": false,
  "code": 400,
  "message": "Invalid JSON format"
}
```

**400 Bad Request (Validation Failed):**

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

**400 Bad Request (Invalid Decimal):**

```json
{
  "success": false,
  "code": 400,
  "message": "Invalid decimal format for nav"
}
```

**404 Not Found (Snapshot):**

```json
{
  "success": false,
  "code": 404,
  "message": "Snapshot with id 123 does not exist"
}
```

**404 Not Found (Account):**

```json
{
  "success": false,
  "code": 404,
  "message": "Account with broker_account_number MT5-789012 does not exist"
}
```

**404 Not Found (Strategy):**

```json
{
  "success": false,
  "code": 404,
  "message": "Strategy with prefix EURUSD_M30 does not exist"
}
```

### 4. Delete Snapshot

**DELETE** `/snapshot/{snapshot_id}/`

Deletes an existing snapshot record.

**Response:**

**200 OK:**

```json
{
  "success": true,
  "message": "Snapshot deleted successfully"
}
```

**404 Not Found:**

```json
{
  "success": false,
  "code": 404,
  "message": "Snapshot with id 123 does not exist"
}
```

## Data Structure

### Snapshot Model

A snapshot record contains the following information:

- **account**: Reference to the associated account (required)
- **strategy**: Reference to the associated strategy (optional, nullable)
- **event**: Description of the event that triggered the snapshot (max 255 characters)
- **nav**: Net Asset Value as a decimal value
- **exposure**: Current exposure amount as a decimal value
- **created_at**: Timestamp when the snapshot was created
- **updated_at**: Timestamp when the snapshot was last updated

## Validation Rules

### broker_account_number

- **Type**: String
- **Required**: Yes (for create), No (for update)
- **Constraints**:
  - Maximum length: 255 characters
  - Cannot be empty
- **Description**: Must reference an existing account's broker account number

### strategy_prefix

- **Type**: String
- **Required**: No
- **Constraints**:
  - Maximum length: 50 characters
  - Cannot be empty (but can be null)
  - Nullable: Yes
- **Description**: Must reference an existing strategy's prefix, or null if no strategy association

### event

- **Type**: String
- **Required**: Yes (for create), No (for update)
- **Constraints**:
  - Maximum length: 255 characters
  - Cannot be empty
- **Description**: Description of the event that triggered the snapshot

### nav

- **Type**: String (decimal format)
- **Required**: Yes (for create), No (for update)
- **Constraints**:
  - Must be a valid decimal number
  - Cannot be empty
- **Description**: Net Asset Value at the time of the snapshot

### exposure

- **Type**: String (decimal format)
- **Required**: Yes (for create), No (for update)
- **Constraints**:
  - Must be a valid decimal number
  - Cannot be empty
- **Description**: Current exposure amount at the time of the snapshot

## Response Format

All API responses follow a consistent format based on the status code:

### Success Responses (2xx)

```json
{
  "success": true,
  "message": "Descriptive success message",
  "data": {} // Optional data payload
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

- **200 OK**: Operation successful (update, delete, search)
- **201 Created**: Snapshot created successfully
- **400 Bad Request**: Invalid request format, validation errors, or invalid decimal format
- **404 Not Found**: Referenced snapshot, account, or strategy not found
- **500 Internal Server Error**: Server error

## Usage Examples

### Creating a Snapshot

```bash
curl -X POST /snapshot/ \
  -H "Content-Type: application/json" \
  -d '{
    "broker_account_number": "MT5-123456",
    "strategy_prefix": "GBPUSD_M15",
    "event": "Position opened",
    "nav": "10000.50",
    "exposure": "2500.75"
  }'
```

### Creating a Snapshot without Strategy

```bash
curl -X POST /snapshot/ \
  -H "Content-Type: application/json" \
  -d '{
    "broker_account_number": "MT5-123456",
    "event": "Account balance updated",
    "nav": "10000.50",
    "exposure": "0.00"
  }'
```

### Searching Snapshots

```bash
# Get all snapshots for a specific account
curl -X GET "/snapshot/search/?broker_account_number=MT5-123456"

# Get snapshots for a specific strategy
curl -X GET "/snapshot/search/?strategy_prefix=GBPUSD_M15"

# Search by event description
curl -X GET "/snapshot/search/?event=Position"

# Combined filters
curl -X GET "/snapshot/search/?broker_account_number=MT5-123456&event=opened"
```

### Updating a Snapshot

```bash
curl -X PUT /snapshot/123/ \
  -H "Content-Type: application/json" \
  -d '{
    "event": "Position modified",
    "nav": "10150.75",
    "exposure": "3000.00"
  }'
```

### Removing Strategy Association

```bash
curl -X PUT /snapshot/123/ \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_prefix": null
  }'
```

### Deleting a Snapshot

```bash
curl -X DELETE /snapshot/123/
```

## Event Types

### Predefined Events (SnapshotEvents Enum)

The system includes predefined event types defined in the `SnapshotEvents` enum:

- `END_OF_DAY_REPORT` (0): Daily report snapshot
- `END_OF_HOUR_REPORT` (1): Hourly report snapshot

### Custom Event Types

You can also use custom event descriptions. Common examples include:

- "Position opened"
- "Position closed"
- "Position modified"
- "Account balance updated"
- "Monthly statement"
- "Margin call triggered"
- "Strategy execution completed"
