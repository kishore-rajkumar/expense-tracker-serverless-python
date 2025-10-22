# IAM Policy Matrix (Expense Tracker Serverless Project)

This matrix defines actor/service permissions for core AWS resources used in the architecture.
Each permission aligns to least-privilege and separation of duties.

## Actor/Service Permissions

Actor/Service    |  Resource             |  Actions Allowed                        |  Rationale/Notes             
-----------------|-----------------------|-----------------------------------------|------------------------------
Cognito User     |  API Gateway          |  execute-api:Invoke(secured endpoints)  |  Authenticated API access    
API Gateway      |  Lambda Functions     |  lambda:InvokeFunction                  |  Routes client requests      
Expenses Lambda  |  DynamoDB (Expenses)  |  GetItem,PutItem,UpdateItem,DeleteItem  |  CRUD operations for expenses
Receipts Lambda  |  S3 (Receipts)        |  PutObject,GetObject                    |  Upload/fetch receipts       
Step Functions   |  Lambda Functions     |  lambda:InvokeFunction                  |  Orchestrate workflow steps  
All Lambdas      |  CloudWatch Logs      |  CreateLogStream,PutLogEvents           |  Logging and monitoring      
Admin Lambda     |  Cognito User Pool    |  AdminCreateUser,AdminGetUser           |  Admin operations (optional) 

### 1. Cognito User → API Gateway
_(API Gateway handles this via built-in authorization, but for completeness, here's a resource policy)_

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:<region>:<account-id>:<rest-api-id>/*/ANY/*"
    }
  ]
}
```

### 2. API Gateway → Lambda Functions
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:<region>:<account-id>:function:<function-name>"
    }
  ]
}
```

### 3. Expenses Lambda → DynamoDB Table (Expenses)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:<region>:<account-id>:table/ExpensesTable"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/expenses:*"
    }
  ]
}
```

### 4. Receipts Lambda → S3 Bucket (Receipts)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::ReceiptsBucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/receipts:*"
    }
  ]
}
```

### 5. Step Functions → Lambda Functions
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:<region>:<account-id>:function:<function-name>"
    }
  ]
}
```

### 6. All Lambdas → CloudWatch Logs
_(Include with each Lambda role)_
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/*"
    }
  ]
}
```

### 7. Admin Lambda → Cognito User Pool
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cognito-idp:AdminCreateUser",
        "cognito-idp:AdminGetUser"
      ],
      "Resource": "arn:aws:cognito-idp:<region>:<account-id>:userpool/<userpool-id>"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/admin:*"
    }
  ]
}
```
