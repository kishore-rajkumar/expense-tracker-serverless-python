# Expense Tracker Serverless Python

![CI](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/actions/workflows/ci-cd.yml/badge.svg)
![License](https://img.shields.io/github/license/kishore-rajkumar/expense-tracker-serverless-python?label=license&style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![AWS](https://img.shields.io/badge/AWS-serverless-yellow?logo=amazon-aws)
![Issues](https://img.shields.io/github/issues/kishore-rajkumar/expense-tracker-serverless-python)

A serverless expense tracking solution built using Python and AWS. Key services: Cognito (auth), DynamoDB, S3, Lambda, API Gateway. Features modular architecture, Infrastructure-as-Code, and automated CI/CD for reliability and scalability.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Onboarding for New Contributors](#onboarding-for-new-contributors)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

---

## Project Overview

**Expense Tracker Serverless Python** lets users track expenses and receipts securely with AWS.  
Designed to demonstrate cloud architecture, clean DevOps, and serverless best practices.

---

## Features

- AWS Cognito user authentication & registration
- Expense/receipt management (DynamoDB, S3)
- Serverless backend with Lambda & API Gateway
- Infrastructure-as-Code using AWS SAM
- Automated GitHub Actions CI/CD pipeline
- Robust error handling, logging, and monitoring

---

## Architecture

See [`docs/architecture.md`](./docs/architecture.md) and [`docs/architecture.png`](./docs/architecture.png).

---

## Getting Started

### Prerequisites

- Python 3.9+
- AWS CLI
- Node.js (for SAM CLI)
- SAM CLI
- Docker (optional, for Lambda testing)

### Setup
```
git clone https://github.com/kishore-rajkumar/expense-tracker-serverless-python.git  
pip install -r requirements.txt  
aws configure  
sam build  
sam deploy --guided  
```

### Run Tests
```
pytest  
flake8 .
```
---

## Onboarding for New Contributors

1. **Review the README and key docs** (see docs links below).
2. **Set up environment:** Python, AWS CLI, Node.js, SAM CLI, Docker (optional).
3. **Clone the repository and install dependencies** as above.
4. **Configure AWS credentials** with `aws configure`.
5. **Run and test locally:** Build/deploy via SAM, run unit/integration tests.
6. **Select an issue/feature:** Browse [Issues](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/issues) or [Projects](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/projects).
7. **Branch and code:** Follow the conventions in [CONTRIBUTING.md](./CONTRIBUTING.md).
8. **Submit a PR:** Reference issues, fill the PR checklist, ensure CI/CD passes.
9. **Ask for help:** Open an Issue or discussion if needed.

---

## Development Workflow

- Project management via GitHub Projects ([see board](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/projects))
- Execution roadmap in [`docs/project-execution-steps-order.md`](./docs/project-execution-steps-order.md)
- Branch/PR rules covered in [`CONTRIBUTING.md`](./CONTRIBUTING.md)

---

## Contributing

We welcome your contributions!

- Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before starting.
- Standard workflow:
  1. Fork + clone repo
  2. Create branch (`feature/<name>`, `bugfix/<name>`, etc.)
  3. Develop, test, and document your changes
  4. Submit PR, fill out the checklist, get review
  5. Ensure CI/CD (lint, tests) passes

---

## Documentation

- [`docs/architecture.md`](./docs/architecture.md): Solution architecture
- [`docs/project-execution-steps-order.md`](./docs/project-execution-steps-order.md): Project steps
- [`docs/ci-cd-pipeline.md`](./docs/ci-cd-pipeline.md): CI/CD pipeline details
- [`docs/auth.md`](./docs/auth.md): Authentication flows

---

## Cognito User Pool Setup

This project uses AWS Cognito User Pool for user authentication, user attribute management, and role-based access control, configured via AWS SAM as Infrastructure as Code.

### User Pool Configuration

- **User Pool Name:** `ExpenseTrackerUserPool`
- **Attributes Enabled:**
  - Email (auto-verified, required, immutable)
  - Username (using email as username)
  - Custom attribute: `name` (required, immutable)
- **Verification:** Email addresses are auto-verified

### User Pool Client Configuration

- **Client Name:** `ExpenseTrackerClient`
- **Authentication Flows Enabled:**
  - ALLOW_USER_PASSWORD_AUTH
  - ALLOW_REFRESH_TOKEN_AUTH
  - ALLOW_USER_SRP_AUTH
- **OAuth Flows Enabled:**
  - Authorization Code Grant (`code`)
  - Implicit Grant (`implicit`)
- **OAuth Scopes:**
  - `email`
  - `openid`
  - `profile`
- **Identity Providers:** Cognito only
- **Callback URLs:** Configured to your deployed frontend URL (replace with actual domain)
- **Logout URLs:** Configured similarly for proper sign-out handling

### User Groups for Role Management

- `admin`
- `user`

Assign users to these groups to manage permissions and access levels within the app.

### API Gateway Integration

- API Gateway is configured with a Cognito User Pool Authorizer as the default authorizer.
- The authorizer validates JWT tokens sent in the `Authorization` header following bearer token format.
- This setup restricts API access to authenticated users in the Cognito User Pool.
- Access control can be enforced based on user groups defined in the pool.

### Environment Variables for Deployment

Ensure these variables are configured correctly in your deployment environment:

- `COGNITO_USER_POOL_ID`: The Cognito User Pool ID (`ExpenseTrackerUserPool`)
- `COGNITO_APP_CLIENT_ID`: The User Pool Client ID (`ExpenseTrackerClient`)
- `AWS_REGION`: AWS region where resources are deployed

### SAM Outputs

After deployment using SAM, the following outputs are available:

- API Gateway URL for production stage endpoint
- Cognito User Pool ID and Client ID for integration
- Cognito Hosted UI URL for user sign-in and authentication flows

### Testing and Maintenance

- Use sample users assigned to groups (`admin`, `user`) to test authentication and role-based access.
- Update SAM templates to adjust user pool configurations or group roles as needed.
- Follow least privilege and security best practices, including use of MFA and secure token handling.



This documentation provides a clear guide for anyone contributing to or operating the expense tracker project on how authentication and authorization is configured via Cognito User Pools and integrated with API Gateway.

---

## Troubleshooting

- CI/CD workflow or setup issues?  
  - Check `.github/workflows/` and [`docs/ci-cd-pipeline.md`](./docs/ci-cd-pipeline.md).
  - See [FAQ](./docs/faq.md) or open an Issue.

---

## Contact

Maintainer: [kishore-rajkumar](https://github.com/kishore-rajkumar)  
Questions? [Open an Issue](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/issues).

---
