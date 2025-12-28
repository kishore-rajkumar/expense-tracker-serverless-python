from unittest.mock import patch, MagicMock
import json
import os
from botocore.exceptions import ClientError
from auth import login

os.environ["COGNITO_CLIENT_ID"] = "test-client-id"
os.environ["AWS_REGION"] = "us-east-1"


def _event(body: dict) -> dict:
    return {
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }


def test_login_requires_username_and_password():
    event = _event({"username": "user@example.com"})  # missing password

    resp = login.handler(event, None)

    assert resp["statusCode"] == 400
    body = json.loads(resp["body"])
    assert body["message"] == "username and password are required"


@patch("boto3.client")
def test_login_success_returns_tokens(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.return_value = {
        "AuthenticationResult": {
            "AccessToken": "access-token",
            "IdToken": "id-token",
            "RefreshToken": "refresh-token",
        }
    }

    event = _event({"username": "user@example.com", "password": "Pass123!"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["accessToken"] == "access-token"
    assert body["idToken"] == "id-token"
    assert body["refreshToken"] == "refresh-token"

    mock_boto_client.assert_called_once()
    mock_cognito.initiate_auth.assert_called_once()


@patch("boto3.client")
def test_login_bad_credentials_returns_401(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.side_effect = ClientError(
        {
            "Error": {
                "Code": "NotAuthorizedException",
                "Message": "Incorrect username or password.",
            }
        },
        "InitiateAuth",
    )

    event = _event({"username": "wrong@example.com", "password": "wrong"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 401


@patch("boto3.client")
def test_login_user_not_found_returns_401(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.side_effect = ClientError(
        {
            "Error": {
                "Code": "UserNotFoundException",
                "Message": "User does not exist.",
            }
        },
        "InitiateAuth",
    )

    event = _event({"username": "nouser@example.com", "password": "Pass123!"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 401
    body = json.loads(resp["body"])
    # adjust to match your actual error message
    assert body["message"] == "incorrect username or password"


@patch("boto3.client")
def test_login_unconfirmed_user_returns_403(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.side_effect = ClientError(
        {
            "Error": {
                "Code": "UserNotConfirmedException",
                "Message": "User is not confirmed.",
            }
        },
        "InitiateAuth",
    )

    event = _event({"username": "user@example.com", "password": "Pass123!"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 403
    body = json.loads(resp["body"])
    assert body["message"] == "user is not confirmed"
    assert body["errorCode"] == "UserNotConfirmedException"


@patch("boto3.client")
def test_password_reset_required_returns_403(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.side_effect = ClientError(
        {
            "Error": {
                "Code": "PasswordResetRequiredException",
                "Message": "Password reset required.",
            }
        },
        "InitiateAuth",
    )

    event = _event({"username": "user@example.com", "password": "oldpass"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 403
    body = json.loads(resp["body"])
    assert body["message"] == "password reset required"
    assert body["errorCode"] == "PasswordResetRequiredException"


@patch("boto3.client")
def test_login_too_many_requests_returns_429(mock_boto_client):
    mock_cognito = MagicMock()
    mock_boto_client.return_value = mock_cognito
    mock_cognito.initiate_auth.side_effect = ClientError(
        {
            "Error": {
                "Code": "TooManyRequestsException",
                "Message": "Rate exceeded",
            }
        },
        "InitiateAuth",
    )

    event = _event({"username": "user@example.com", "password": "Pass123!"})

    resp = login.handler(event, None)

    assert resp["statusCode"] == 429
    body = json.loads(resp["body"])
    assert body["message"] == "too many attempts, please try again later"
    assert body["errorCode"] == "TooManyRequestsException"


def test_login_with_apigw_proxy_event_shape():
    body = {"username": "user@example.com", "password": "Pass123!"}
    event = {
        "resource": "/auth/login",
        "path": "/auth/login",
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "queryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }

    # use existing success mocking helper / patch
    with patch("boto3.client") as mock_boto_client:
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        mock_cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "AccessToken": "access-token",
                "IdToken": "id-token",
                "RefreshToken": "refresh-token",
            }
        }

        resp = login.handler(event, None)

    assert resp["statusCode"] == 200
