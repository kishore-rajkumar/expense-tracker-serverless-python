# Authentication Setup (AWS Cognito)

## 1. Purpose

This project uses **AWS Cognito User Pool** for basic user authentication (signup, login, JWT for API access).

## 2. Setup Steps

- **Create a User Pool** in AWS Console (or via Infrastructure-as-Code if used)
  - Note your User Pool name and region.
- **Create an App Client** (ensure “no client secret” is selected)
  - Note your App Client ID.

## 3. Required Configuration

Add the following variables to your `.env` file (or preferred secrets manager):
```
COGNITO_USER_POOL_ID=your_pool_id
COGNITO_APP_CLIENT_ID=your_app_client_id
COGNITO_REGION=your_region
```

## 4. Usage

- **Frontend**:  
  Use the Cognito hosted UI, AWS Amplify, or your own signup/login page to let users sign up or sign in and receive a JWT token.
- **Backend/API**:  
  Supply the JWT token in the `Authorization` header to protected endpoints.  
  API Gateway uses a Cognito Authorizer to validate tokens.

## 5. Troubleshooting

- **Invalid token:**  
  Ensure App Client ID and User Pool ID are correct and match the region.
- **User not found:**  
  Check that you are using the correct user pool and region.

## 6. Local Login Testing (SAM + Cognito)

This project includes a helper script to locally invoke the `LoginFunction` Lambda using `sam local`, with the correct Cognito User Pool ClientId automatically fetched from CloudFormation.

### Prerequisites

- AWS CLI configured (`aws --version`)
- AWS SAM CLI installed (`sam --version`)
- Docker Desktop running
- A deployed dev stack (creates the Cognito UserPool + UserPoolClient). For example:

`sam build`   
`sam deploy --config-env dev`

### One-time setup

- Ensure the dev stack name and region in the script match your environment:
```infrastructure/scripts/sam_local_invoke_login.py
STACK_NAME = "expense-tracker-dev" # adjust if needed
FUNCTION_NAME = "LoginFunction"
REGION = "us-east-1"
```

- `infrastructure/env.local.json` is **generated** and should remain ignored (already listed in `.gitignore`).

### Running local login tests

From the repository root:

`python infrastructure/scripts/sam_local_invoke_login.py`

This script will:

1. Call `aws cloudformation describe-stack-resources` to resolve the physical Cognito app ClientId from the `ExpenseTrackerUserPoolClient` logical ID.
2. Generate `infrastructure/env.local.json` with:

```
{
   "LoginFunction": {
     "COGNITO_CLIENT_ID": "<resolved-client-id>",
     "AWS_REGION": "<region>"
   }
}
```

3. Run:

```
sam local invoke LoginFunction
-t infrastructure/template.yaml
-e infrastructure/events/login_success.json
--env-vars infrastructure/env.local.json
--region <region>
```

If everything is configured correctly, the output should be a `200` response with Cognito tokens in the body.

### Event fixture

The `infrastructure/events/login_success.json` file contains an API Gateway proxy event for a successful login request. You can duplicate and tweak this file (e.g., wrong password, missing fields) to exercise other paths in `LoginFunction`.

## 7. References

- [AWS Cognito User Pools documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
