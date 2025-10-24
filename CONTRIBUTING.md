# Contributing to Expense Tracker Serverless Python

Thank you for your interest in making this project better!  
This document guides you through the standards and process for effective contributions.

---

## 1. Introduction

Please read these guidelines before submitting changes.  
Following these standards will ensure high code quality and a smooth review workflow.

This document covers:
- Coding style and formatting
- Branching strategies
- Pull Request (PR) submission and review
- Testing requirements
- Continuous Integration (CI) standards

---

## 2. Coding Standards

- Use `black` for formatting and `flake8` for linting Python code.
- Follow [PEP 8](https://pep8.org/) for code style and [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings.
- Write clear, descriptive comments and maintain concise, readable code.
- Naming conventions:
  - `snake_case` for functions/variables.
  - `PascalCase` for classes.
  - All folders and filenames should be lowercase, using hyphens or underscores as needed.

---

## 3. Branching Strategy

- Branch from `main` or `develop`.
- Recommended naming:
  - `feature/<short-description>`
  - `bugfix/<short-description>`
  - `release/<version>`
- Link every branch to a relevant GitHub Issue for traceability.

---

## 4. Pull Request Guidelines

- Create PRs against `main` or `develop` only.
- Complete the PR Review Checklist (see below) and reference related issues in the PR description.
- Each PR must pass CI (linting, tests).
- At least **one reviewer approval** is required before merging.
- Direct pushes to `main` are prohibited—always use PRs.

---

## 5. Testing Standards

- All new features and bug fixes must have adequate unit or integration test coverage.
- Aim for **80%+ overall test coverage**.
- Use `pytest` or `unittest` for test suites.
- Run all tests locally before submitting a PR.

---

## 6. CI/CD Pipeline

- All PRs must pass:
  - Lint checks (`flake8`)
  - Format checks (`black`)
  - Test suite (`pytest`)
  - Optional: code coverage checks
- For more details, see [`docs/ci-cd-pipeline.md`](./docs/ci-cd-pipeline.md).

---

## 7. Pull Request Review Checklist

Please ensure the following items are checked before submitting a PR:

- [ ] Code follows style guidelines (`black`, `flake8`)
- [ ] Docstrings/comments are added or updated as needed
- [ ] Tests are added/updated and pass locally
- [ ] Documentation updated where required
- [ ] Linked issue referenced in PR
- [ ] CI checks pass before merge

---

## 8. Suggestions and Issues

- For major changes, open an Issue first to discuss your proposal.
- For questions or suggestions, raise a discussion or contact the maintainers.

---
