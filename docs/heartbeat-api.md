# Heartbeat API Documentation

The Heartbeat API provides endpoints for managing system heartbeat events within the Horizon Router system. Heartbeats are used to track activity and events across different accounts and strategies.

## Base URL

All endpoints are prefixed with the API base URL.

## Endpoints

### 1. Create Heartbeat

**POST** `/heartbeat/`

Creates a new heartbeat event record and automatically cleans up heartbeats older than 7 days.

**Request Body:**

```json
{
  "broker_account_number": "MT5-123456", // Required, string, max 255 chars, cannot be empty
  "strategy_prefix": "GBPUSD_M15", // Required, string, max 50 chars, cannot be empty
  "event": "Strategy executed successfully" // Required, string, max 255 chars, cannot be empty
}
```

**Response:**

**201 Created:**

```json
{
  "success": true,
  "message": "Heartbeat created successfully"
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

## Data Structure

### Heartbeat Model

A heartbeat record contains the following information:

- **account**: Reference to the associated account
- **strategy**: Reference to the associated strategy
- **event**: Description of the event (max 255 characters)
- **created_at**: Timestamp when the heartbeat was created
- **updated_at**: Timestamp when the heartbeat was last updated

## Validation Rules

### broker_account_number

- **Type**: String
- **Required**: Yes
- **Constraints**:
  - Maximum length: 255 characters
  - Cannot be empty
- **Description**: Must reference an existing account's broker account number

### strategy_prefix

- **Type**: String
- **Required**: Yes
- **Constraints**:
  - Maximum length: 50 characters
  - Cannot be empty
- **Description**: Must reference an existing strategy's prefix

### event

- **Type**: String
- **Required**: Yes
- **Constraints**:
  - Maximum length: 255 characters
  - Cannot be empty
- **Description**: Description of the heartbeat event

## Automatic Cleanup

The system automatically performs cleanup operations when creating heartbeats:

- **Retention Period**: 7 days
- **Cleanup Trigger**: Executed on each heartbeat creation
- **Action**: Deletes all heartbeat records older than 7 days from the current timestamp

## Response Format

All API responses follow a consistent format based on the status code:

### Success Responses (2xx)

```json
{
  "success": true,
  "message": "Descriptive success message"
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

- **201 Created**: Heartbeat created successfully
- **400 Bad Request**: Invalid request format or validation errors
- **404 Not Found**: Referenced account or strategy not found
- **500 Internal Server Error**: Server error

## Usage Examples

### Creating a Heartbeat

```bash
curl -X POST /heartbeat/ \
  -H "Content-Type: application/json" \
  -d '{
    "broker_account_number": "MT5-123456",
    "strategy_prefix": "GBPUSD_M15",
    "event": "Strategy execution completed"
  }'
```

### Common Event Types

Typical heartbeat events might include:

- "Strategy started"
- "Strategy execution completed"
- "Deal opened"
- "Deal closed"
- "Error occurred"
- "System check passed"
