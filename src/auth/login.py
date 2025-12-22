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

    _cognito = boto3.client("cognito-idp", region_name=_REGION)

    try:
        result = _cognito.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=_CLIENT_ID,
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
        )
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "ClientError")
        message = error.get("Message", str(exc))
        status = 401 if code in {"NotAuthorizedException", "UserNotFoundException"} else 500
        return _response(status, {"errorCode": code, "message": message})

    auth = result.get("AuthenticationResult", {})
    return _response(
        200,
        {
            "accessToken": auth.get("AccessToken"),
            "idToken": auth.get("IdToken"),
            "refreshToken": auth.get("RefreshToken"),
        },
    )
