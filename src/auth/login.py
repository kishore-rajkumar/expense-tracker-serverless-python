import json
import os
import boto3
from botocore.exceptions import ClientError


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }


def handler(event, _context):
    _CLIENT_ID = os.environ["COGNITO_CLIENT_ID"]
    _REGION = os.environ.get("AWS_REGION", "us-east-1")

    if not _CLIENT_ID:
        return _response(500, {"message": "COGNITO_CLIENT_ID is not configured"})

    body_raw = event.get("body") or ""
    try:
        data = json.loads(body_raw)
    except json.JSONDecodeError:
        return _response(400, {"message": "Invalid JSON body"})

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return _response(400, {"message": "username and password are required"})

    status, body = authenticate_user(username, password, _CLIENT_ID, _REGION)
    return _response(status, body)


def authenticate_user(username: str, password: str, client_id: str, region: str):
    cognito = boto3.client("cognito-idp", region_name=region)

    try:
        result = cognito.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=client_id,
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
        )
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "ClientError")

        status = 500
        message = "internal server error"

        if code in {"NotAuthorizedException", "UserNotFoundException"}:
            status = 401
            message = "incorrect username or password"
        elif code == "UserNotConfirmedException":
            status = 403
            message = "user is not confirmed"
        elif code == "PasswordResetRequiredException":
            status = 403
            message = "password reset required"

        return status, {"errorCode": code, "message": message}

    auth = result.get("AuthenticationResult", {})
    return 200, {
        "accessToken": auth.get("AccessToken"),
        "idToken": auth.get("IdToken"),
        "refreshToken": auth.get("RefreshToken"),
    }
