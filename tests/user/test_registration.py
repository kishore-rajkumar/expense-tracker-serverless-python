import json
from unittest.mock import patch
# import pytest
from user.registration import lambda_handler  # Import the function to be tested


# Define a custom exception class to simulate
# the AWS Cognito UsernameExistsException.
# It inherits from Python's base Exception class
# to be usable in try-except blocks.
class MockUsernameExistsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)


def test_successful_registration(monkeypatch):
    # Prepare a fake event with valid registration data
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "password": "validPassword123",
            "name": "Test User"
        })
    }

    # Set up environment variables as in Lambda
    monkeypatch.setenv('USER_POOL_ID', 'test-pool-id')
    monkeypatch.setenv('CLIENT_ID', 'test-client-id')

    # Patch boto3 client and sign_up method
    with patch('boto3.client') as mock_client:
        mock_cognito = mock_client.return_value
        mock_cognito.sign_up.return_value = {"UserConfirmed": False}
        response = lambda_handler(event, None)

        # Assert sign_up was actually called
        mock_cognito.sign_up.assert_called_once_with(
            ClientId='test-client-id',
            Username='test@example.com',
            Password='validPassword123',
            UserAttributes=[
                {'Name': 'email', 'Value': 'test@example.com'},
                {'Name': 'name', 'Value': 'Test User'}
            ]
        )

        # Expect HTTP 201 Created
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert "User registered successfully" in body['message']


def test_username_exists_exception(monkeypatch):
    # Prepare a fake event with valid registration data
    event = {
        "body": json.dumps({
            "email": "existing@example.com",
            "password": "validPassword123",
            "name": "Existing User"
        })
    }
    monkeypatch.setenv('USER_POOL_ID', 'test-pool-id')
    monkeypatch.setenv('CLIENT_ID', 'test-client-id')

    with patch('boto3.client') as mock_client:
        mock_cognito = mock_client.return_value

        # Set up the mock Cognito client's exceptions attribute with
        # our custom UsernameExistsException class.
        mock_cognito.exceptions = type('Exceptions', (), {'UsernameExistsException': MockUsernameExistsException})()

        # Set the sign_up method to raise the UsernameExistsException
        # when called, simulating an existing user error from Cognito.
        mock_cognito.sign_up.side_effect = mock_cognito.exceptions.UsernameExistsException("User already exists")

        response = lambda_handler(event, None)

        assert response['statusCode'] == 409
        body = json.loads(response['body'])
        assert "User already exists" in body['message']


def test_invalid_email():
    event = {
        "body": json.dumps({
            "email": "invalid-email",
            "password": "validPassword123",
            "name": "Test User"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    assert "Invalid or missing email" in response['body']


def test_invalid_password():
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "password": "short",
            "name": "Test User"
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    assert "Password does not meet criteria" in response['body']


def test_missing_name():
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "password": "validPassword123"
            # name is missing
        })
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    assert "Name is required" in response['body']
