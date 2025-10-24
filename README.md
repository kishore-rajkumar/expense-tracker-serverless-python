# Expense Tracker Serverless Python

![CI](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/actions/workflows/main.yml/badge.svg)
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

## Troubleshooting

- CI/CD workflow or setup issues?  
  - Check `.github/workflows/` and [`docs/ci-cd-pipeline.md`](./docs/ci-cd-pipeline.md).
  - See [FAQ](./docs/faq.md) or open an Issue.

---

## Contact

Maintainer: [kishore-rajkumar](https://github.com/kishore-rajkumar)  
Questions? [Open an Issue](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/issues).

---
