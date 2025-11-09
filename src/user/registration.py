import json
import boto3
import re
import os

cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = os.environ.get('USER_POOL_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # Implement password strength rules here, e.g., min length
    return len(password) >= 8

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        email = body.get('email')
        password = body.get('password')
        name = body.get('name')

        if not email or not validate_email(email):
            return response(400, {'message': 'Invalid or missing email.'})
        if not password or not validate_password(password):
            return response(400, {'message': 'Password does not meet criteria.'})
        if not name:
            return response(400, {'message': 'Name is required.'})

        # Register user in Cognito user pool
        resp = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': name}
            ]
        )

        return response(201, {'message': 'User registered successfully. Please confirm your email if required.'})

    except cognito_client.exceptions.UsernameExistsException:
        return response(409, {'message': 'User already exists.'})
    except cognito_client.exceptions.InvalidPasswordException:
        return response(400, {'message': 'Password does not meet complexity requirements.'})
    except Exception as e:
        return response(500, {'message': 'Internal server error.', 'error': str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }
