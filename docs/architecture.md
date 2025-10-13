# AWS Serverless Architecture for Expense Tracker Application

## Architecture Diagram

![Serverless Architecture Diagram](architecture.png)

---

## Architecture Overview

This diagram illustrates the AWS serverless architecture designed for a scalable and secure expense tracking application.

### Components and Data Flow:

- **Clients (Web/Mobile App):**
  - Users initiate requests such as adding expenses or uploading receipts.
  - They interact with the app interface which communicates via HTTP requests.

- **API Gateway:**
  - Acts as the front-door for all incoming requests.
  - Routes requests to appropriate Lambda functions after performing validation and throttling.
  - Manages API-level security, rate limiting, and request shaping.

- **AWS Cognito (Authentication & Authorization):**
  - Handles user sign-up, login, and token management.
  - Verifies user identity and issues JWT tokens for secure access.
  - Ensures only authenticated users can access protected resources.

- **AWS Lambda (Business Logic):**
  - Executes core application logic, such as CRUD operations on expenses.
  - Processes receipt uploads and metadata management.
  - Interacts with DynamoDB and S3 to store and retrieve data.

- **Amazon DynamoDB (Data Storage):**
  - Stores expense records, user profiles, and metadata.
  - A fast, scalable NoSQL database optimized for serverless apps.

- **Amazon S3 (File Storage):**
  - Stores receipt images and documents.
  - Receipts are uploaded here and referenced via URLs stored in DynamoDB.

- **Amazon CloudWatch (Monitoring & Logging):**
  - Collects logs from Lambda and API Gateway.
  - Provides metrics, dashboards, and alerts to monitor system health and troubleshoot issues.

---

## Project Folder Structure

This section describes the recommended organization for the AWS serverless expense tracker application:
```
expense-tracker-serverless-python/
├── docs/
│ ├── architecture.md # AWS architecture and system overview
│ ├── architecture.png # Architecture diagram image
│ ├── user-guide.md # End user instructions
│ └── api-reference.md # API endpoint documentation
├── src/
│ ├── expenses/ # Lambda for expense CRUD operations
│ ├── receipts/ # Lambda for receipt uploads
│ ├── approval/ # Lambda for approval workflow
│ └── common/ # Shared utilities
├── workflows/
│ └── expenseApproval.asl.json # Step Functions workflow definition (ASL)
├── infrastructure/
│ ├── template.yaml # AWS SAM/CloudFormation template
│ └── dynamodb-table.yaml # DynamoDB setup/configuration
├── tests/
│ ├── expenses/ # Tests for expenses Lambda
│ ├── receipts/ # Tests for receipts Lambda
│ ├── approval/ # Tests for approval Lambdas
│ └── common/ # Tests for utilities
├── .github/
│ └── workflows/
│ └── ci-cd.yaml # CI/CD pipeline automation
├── README.md # Project summary and main instructions
├── requirements.txt / package.json # Project dependencies
└── .env.example # Sample environment variables
```

This structure separates source code, infrastructure as code, workflows, documentation, and tests for clarity, maintainability, and easy team collaboration.

---

## Summary

This architecture ensures a highly scalable, cost-efficient, and secure expense tracking system, leveraging AWS serverless services to reduce operational overhead, enhance performance, and facilitate future growth.

---

Feel free to request additional documentation sections or further simplifications as needed.
