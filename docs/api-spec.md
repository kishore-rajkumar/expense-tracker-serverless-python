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

(Diagram or visual table can be added here.)

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
- Description: Retrieve all expenses for the authenticated user.
- Auth: Required
- Response Schema:
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
- Retrieves a single expense by ID.

#### PUT /expenses/{expenseId}
- Updates an expense entry.

#### DELETE /expenses/{expenseId}
- Removes an expense.

---

### 2. Receipts

#### POST /receipts
- Uploads a receipt for a given expense.

#### GET /receipts/{receiptId}
- Retrieves a receipt by ID.

#### DELETE /receipts/{receiptId}
- Deletes a receipt.

---

### 3. Users

#### POST /users/register
- Registers a new user (for admin/manual onboarding).

#### GET /users/{userId}
- Retrieves profile data.

#### PUT /users/{userId}
- Updates user profile.

---

## Error Handling
All endpoints return errors in the following format:
```
{
"status": "error",
"error": {
"code": "EXPENSE_NOT_FOUND",
"message": "Expense not found."
}
}
```

---

## Example Requests/Responses
(Add examples for each critical endpoint here.)

---

## Changelog
- `2025-10-10`: Initial API spec created (Expenses, Receipts, Users v1).

