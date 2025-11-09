import json
import pytest
from user.registration import lambda_handler  # Import the function to be tested

def test_successful_registration(monkeypatch):
    # Prepare a fake event with valid registration data
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "password": "validPassword123",
            "name": "Test User"
        })
    }

    # Mock boto3 client and sign_up call here (to be implemented)
    # For now, just check structure of response

    response = lambda_handler(event, None)

    # Expect HTTP 201 Created
    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    assert "User registered successfully" in body['message']
