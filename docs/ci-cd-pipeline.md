# CI/CD Pipeline Overview

This document describes the CI/CD automation used in the expense-tracker-serverless-python project. 
The pipeline is implemented using GitHub Actions and deploys the AWS SAM serverless application on every push or pull request to the main branch.

## Workflow Triggers
- Push to main
- Pull Request targeting main

## Pipeline Steps

**1. Checkout Source**
  - Retrieves the latest code from the repository.

**2. Set Up Python Environment**
  - Uses actions/setup-python to specify Python 3.11 (edit as needed).

**3. Install Project Dependencies**
  - Installs dependencies listed in requirements.txt including aws-sam-cli, flake8, pytest.

**4. Run Static Code Analysis**
  - Executes flake8 to ensure code quality and adherence to style guidelines.
  - Configuration is managed via the .flake8 file.

**5. Run Unit Tests**
  - Executes pytest for automated test coverage.

**6. Configure AWS Credentials**
  - Uses the aws-actions/configure-aws-credentials action to provide credentials (access/secret keys stored as GitHub Secrets).

**7. Build Application**
  - Runs sam build to package the serverless application for deployment.

**8. Deploy to AWS**
  - Executes sam deploy to create/update the stack in your AWS account.

## Secrets & Environment Variables
The following secrets must be set in your GitHub repository:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY

## Set your AWS region as needed (default is ap-south-1).

### Key Project Files
  - .github/workflows/deploy.yml (GitHub Actions workflow YAML)
  - requirements.txt (project dependencies)
  - .flake8 (linting configuration)

## Example Workflow YAML
See .github/workflows/deploy.yml for the full, up-to-date pipeline configuration.

## Modifying or Extending the Pipeline
  - Update requirements.txt for new dependencies.
  - Customize .flake8 for stricter or project-specific linting rules.
  - Add additional steps for integration, security (e.g., bandit), or deployment environments (e.g., staging/production).

## References
  - [GitHub Actions Documentation](https://docs.github.com/en/actions)
  - [AWS SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
