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

## 6. References

- [AWS Cognito User Pools documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
