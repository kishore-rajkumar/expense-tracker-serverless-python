# Architecture Overview

## High-Level Diagram

- User authenticates via AWS Cognito
- API Gateway exposes REST endpoints
- Lambda functions (Python) handle business logic
- DynamoDB for expense data
- S3 for storing receipt images
- Step Functions for expense workflow

(Diagram to be added)

## Component List
- Cognito: User authentication
- API Gateway: REST API
- Lambda: Business logic (Python)
- DynamoDB: Expense data storage
- S3: Receipt uploads
- Step Functions: Expense approval/status flow
