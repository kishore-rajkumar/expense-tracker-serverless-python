# Expense Tracker API Specification

## Table of Contents
- [Introduction](#introduction)
- [Authentication & Authorization](#authentication--authorization)
- [Entity Overview & Relationships](#entity-overview--relationships)
- [API Endpoints](#api-endpoints)
  - [Expenses](#1-expenses)
  - [Receipts](#2-receipts)
  - [Users](#3-users)
- [Error Handling](#error-handling)
- [Example Requests/Responses](#example-requestsresponses)
- [Changelog](#changelog)

---

## Introduction
This API powers the expense tracker serverless SaaS, providing endpoints for managing expenses, receipts, and user profiles in a secure, scalable manner.

## Authentication & Authorization
- All endpoints require a valid **Cognito JWT** token in the `Authorization: Bearer <token>` header.
- User-level authentication is enforced on all resources.
- Admin endpoints may be added in future releases.

## Entity Overview & Relationships

### Entities

| Entity   | Attributes                                             | Relationships                       |
|----------|-------------------------------------------------------|-------------------------------------|
| User     | userId, name, email, registrationDate                  | hasMany: Expenses                   |
| Expense  | expenseId, userId, amount, category, date, description | belongsTo: User; hasMany: Receipts  |
| Receipt  | receiptId, expenseId, fileUrl, uploadedAt              | belongsTo: Expense                  |


<br/>
<img width="1089" height="257" alt="image" src="https://github.com/user-attachments/assets/7678e615-a2c1-48df-8943-72924fc88bcc" />

---

## API Endpoints

### 1. Expenses

#### POST /expenses
- **Description:** Create a new expense entry for the authenticated user.
- **Auth:** Required (Cognito JWT)
- **Request Schema:**
`{
  "amount": 123.45,
  "category": "Travel",
  "date": "2025-10-10",
  "description": "Uber to airport",
  "receiptId": "optional-receipt-id"
}`

- **Response:**
`
{
  "expenseId": "abc123",
  "status": "success"
}
`

#### GET /expenses
- **Description:** Retrieve all expenses for the authenticated user.
- **Auth:** Required
- **Response Schema:**
 `[
  {
    "expenseId": "abc123",
    "amount": 123.45,
    "category": "Travel",
    "date": "2025-10-10",
    "description": "Uber to airport",
    "receiptUrl": "https://bucket/file.jpg"
  },
  ...
]`


#### GET /expenses/{expenseId}
- **Description:** Retrieve a single expense by ID.
- **Auth:** Required
- **Response Schema:**
  `
  {
  "expenseId": "abc123",
  "amount": 123.45,
  "category": "Travel",
  "date": "2025-10-10",
  "description": "Uber to airport",
  "userId": "user123",
  "receiptUrl": "https://bucket/file.jpg"
}
`

#### PUT /expenses/{expenseId}
- **Description:** Update an expense by ID.
- **Auth:** Required
- **Request Schema:** (fields to update)
`
{
  "amount": 130.00,
  "category": "Business Travel"
}
`
- **Response Schema:**
`
{
  "expenseId": "abc123",
  "status": "updated"
}
`

#### DELETE /expenses/{expenseId}
- **Description:** Delete an expense by ID.
- **Auth:** Required
- **Response Schema:**
`
{
  "expenseId": "abc123",
  "status": "deleted"
}
`
---

### 2. Receipts

#### POST /receipts
- **Description:** Upload a receipt for a specific expense.
- **Auth:** Required (Cognito JWT)
- **Request**: multipart/form-data
    - Fields:
        - expenseId: string (required) – Expense to link receipt to
        - file: binary (required) – The receipt image/PDF file
- **Response Schema:**
`
{
  "receiptId": "rct789",
  "expenseId": "exp123",
  "fileUrl": "https://bucket/receipts/rct789.jpg",
  "uploadedAt": "2025-10-11T19:22:30Z",
  "status": "success"
}
`
#### GET /receipts/{receiptId}
- **Description:** Retrieve details and URL for a receipt by its ID.
- **Auth:** Required
- **Response Schema:**
`
{
  "receiptId": "rct789",
  "expenseId": "exp123",
  "fileUrl": "https://bucket/receipts/rct789.jpg",
  "uploadedAt": "2025-10-11T19:22:30Z"
}
`

#### DELETE /receipts/{receiptId}
- **Description:** Delete a receipt by its ID; also removes file from storage.
- **Auth:** Required
- **Response Schema:**
`
{
  "receiptId": "rct789",
  "status": "deleted"
}
`

---

### 3. Users

#### POST /users/register
- **Description:** Registers a new user account. (For manual onboarding, admin flows, or extension beyond Cognito)
- **Auth:** Not required for registration
- **Request Schema:**
`
{
  "name": "Kishore Rajkumar",
  "email": "kishore@example.com",
  "password": "userpassword123"
}
`
- **Response Schema:**
`
{
  "userId": "u123",
  "status": "registered"
}
`

#### GET /users/{userId}
- **Description:** Retrieves user profile details by ID.
- **Auth:** Required (Cognito JWT)
- **Response Schema:**
`
{
  "userId": "u123",
  "name": "Kishore Rajkumar",
  "email": "kishore@example.com",
  "registrationDate": "2025-10-11T12:00:00Z"
}
`
#### PUT /users/{userId}
- **Description:** Updates user profile information.
- **Auth:** Required
- **Request Schema:**
`
{
  "name": "Kishore R.",
  "email": "newmail@example.com"
}
`
- **Response Schema:**
`
{
  "userId": "u123",
  "status": "updated"
}
`

---

## Error Handling
All endpoints return errors in the following format:
```
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error description."
  }
}

```
#### Fields:
- **status:** Always "error" for error responses.
- **error.code:** Machine-friendly string for identifying the error type.
- **error.message:** Description to be shown or logged, user- and developer-friendly.

### Example Error Responses

**Validation Error (400)**
```
{
  "status": "error",
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Amount must be a positive number."
  }
}
```

**Resource Not Found (404)**
```
{
  "status": "error",
  "error": {
    "code": "EXPENSE_NOT_FOUND",
    "message": "No expense found with the given ID."
  }
}
```
**Unauthorized (401)**
```
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Authentication is required for this endpoint."
  }
}
```

**Forbidden (403)**
```
{
  "status": "error",
  "error": {
    "code": "ACCESS_DENIED",
    "message": "You do not have permission to update this resource."
  }
}
```

**Internal Server Error (500)**
```
{
  "status": "error",
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected server error occurred. Please try again later."
  }
}
```

### Error Code Reference
- VALIDATION_FAILED
- EXPENSE_NOT_FOUND
- RECEIPT_NOT_FOUND
- USER_NOT_FOUND
- AUTH_REQUIRED
- ACCESS_DENIED
- INTERNAL_ERROR

_Clients should always check for the **"status": "error"** property and handle display or retries accordingly._

---

## Example Requests/Responses

#### Create an Expense
- **Request:** POST /expenses
```
{
  "amount": 250.00,
  "category": "Meals",
  "date": "2025-10-11",
  "description": "Business lunch with client"
}
```
- **Successful Response:**
```
{
  "expenseId": "exp12345",
  "status": "success"
}
```

#### Retrieve All Expenses

- **Request:** GET /expenses

- **Successful Response:**
```
[
  {
    "expenseId": "exp12345",
    "amount": 250.00,
    "category": "Meals",
    "date": "2025-10-11",
    "description": "Business lunch with client",
    "receiptUrl": "https://bucket/receipt1.jpg"
  },
  {
    "expenseId": "exp12346",
    "amount": 80.75,
    "category": "Transport",
    "date": "2025-10-10",
    "description": "Uber ride",
    "receiptUrl": "https://bucket/receipt2.jpg"
  }
]
```

#### Upload a Receipt

- **Request:** POST /receipts (multipart/form-data)
  - **expenseId:** "exp12345"
  - **file:** [Receipt image file]
- **Successful Response:**
```
{
  "receiptId": "rec98765",
  "expenseId": "exp12345",
  "receiptUrl": "https://bucket/receipt98765.jpg",
  "uploadedAt": "2025-10-11T18:22:11Z",
  "status": "success"
}
```

#### Register a User
- **Request:** POST /users/register
```
{
  "name": "Kishore Rajkumar",
  "email": "kishore@example.com",
  "password": "secretpassword"
}
```
- **Successful Response:**
```
{
  "userId": "user001",
  "status": "registered"
}
```

### Get User Profile
- **Request:** GET /users/user001
- **Successful Response:**
```
{
  "userId": "user001",
  "name": "Kishore Rajkumar",
  "email": "kishore@example.com",
  "registrationDate": "2025-10-11T13:40:00Z"
}
```

---

## Changelog
- `2025-10-10`: Initial API spec created (Expenses, Receipts, Users v1).


---

## Changelog

| Date       | Version | Description                                    | Author           |
|------------|---------|------------------------------------------------|------------------|
| 2025-10-10 | 1.0     | Initial API spec created with Expenses, Receipts, Users endpoints. | Kishore Rajkumar |
| 2025-10-11 | 1.1     | Added detail in the API spec (Expenses, Receipts, Users) ; Added detailed error handling section and example requests/responses. | Kishore Rajkumar |


