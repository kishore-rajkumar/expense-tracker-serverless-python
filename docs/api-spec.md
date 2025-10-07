
# API Specification

## Endpoints

### `POST /expenses`
- **Description:** Create a new expense
- **Auth:** Cognito JWT required
- **Request Body:** `{ "amount": float, "category": str, "date": str, "description": str }`
- **Response:** `{ "expenseId": str, ... }`

### `GET /expenses`
- **Description:** Retrieve user’s expenses
- **Auth:** Cognito JWT required
- **Response:** `[ { "expenseId": str, "amount": float, ... } ]`

### `POST /receipts`
- **Description:** Upload a receipt image
- **Auth:** Cognito JWT required
- **Request:** Multipart/form-data
- **Response:** `{ "receiptUrl": str }`

(More endpoints to be designed iteratively)
