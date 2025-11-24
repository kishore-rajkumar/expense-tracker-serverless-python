import json
import os
from unittest.mock import patch
# import pytest
from user.registration import lambda_handler

# Setup environment variables needed for your Lambda
os.environ['USER_POOL_ID'] = 'test_pool'
os.environ['CLIENT_ID'] = 'test_client'
os.environ['REGISTRATION_MODE'] = 'SignUp'


def make_event(body_dict):
    return {'body': json.dumps(body_dict)}


# Mock Cognito client with basic user registration state
class MockCognitoClient:
    def __init__(self):
        self.users = {}

    def sign_up(self, ClientId, Username, Password, UserAttributes):
        if Username in self.users:
            raise self.exceptions.UsernameExistsException({'Error': {'Code': 'UsernameExistsException'}}, 'sign_up')
        self.users[Username] = {'Password': Password, 'Attributes': UserAttributes}
        return {'UserConfirmed': False}

    def admin_create_user(self, UserPoolId, Username, UserAttributes, MessageAction=None):
        if Username in self.users:
            raise self.exceptions.UsernameExistsException(
                {'Error': {'Code': 'UsernameExistsException'}}, 'admin_create_user')
        self.users[Username] = {'Attributes': UserAttributes, 'Password': None}

    def admin_set_user_password(self, UserPoolId, Username, Password, Permanent=True):
        if Username not in self.users:
            raise Exception('User does not exist')
        self.users[Username]['Password'] = Password

    class exceptions:
        class UsernameExistsException(Exception):
            pass


@patch('boto3.client')
def test_registration_flow(mock_boto_client):
    # Arrange: patch boto3 client to use our mock
    mock_client = MockCognitoClient()
    mock_boto_client.return_value = mock_client

    # Act & Assert patterns
    # 1. Valid registration succeeds
    event = make_event({'email': 'user@example.com', 'password': 'SecurePass123', 'name': 'Test User'})
    response = lambda_handler(event, None)
    assert response['statusCode'] == 201
    assert json.loads(response['body'])['message'] == 'User registered successfully'

    # 2. Duplicate registration returns conflict
    response2 = lambda_handler(event, None)
    assert response2['statusCode'] == 409
    assert 'User already exists' in json.loads(response2['body'])['message']

    # 3. Invalid email gives client error
    bad_email_event = make_event({'email': 'bad-email', 'password': 'SecurePass123', 'name': 'Test User'})
    response3 = lambda_handler(bad_email_event, None)
    assert response3['statusCode'] == 400
    assert 'Invalid or missing email' in json.loads(response3['body'])['message']

    # 4. Weak password gives client error
    weak_pass_event = make_event({'email': 'user2@example.com', 'password': 'short', 'name': 'Test User'})
    response4 = lambda_handler(weak_pass_event, None)
    assert response4['statusCode'] == 400
    assert 'Password does not meet criteria' in json.loads(response4['body'])['message']

    # 5. Missing name gives client error
    missing_name_event = make_event({'email': 'user3@example.com', 'password': 'SecurePass123'})
    response5 = lambda_handler(missing_name_event, None)
    assert response5['statusCode'] == 400
    assert 'Name is required' in json.loads(response5['body'])['message']


@patch('boto3.client')
def test_admin_create_user_registration(mock_boto_client):
    mock_client = MockCognitoClient()
    mock_boto_client.return_value = mock_client

    # Set environment variable for AdminCreateUser mode
    os.environ['REGISTRATION_MODE'] = 'AdminCreateUser'

    event = make_event({'email': 'adminuser@example.com', 'password': 'AdminPass123', 'name': 'Admin User'})

    # First create user - expect success
    response = lambda_handler(event, None)
    assert response['statusCode'] == 201
    assert 'User registered successfully' in json.loads(response['body'])['message']

    # Duplicate user should raise conflict error
    response2 = lambda_handler(event, None)
    assert response2['statusCode'] == 409
