import json
import os
import boto3
import time
from botocore.exceptions import ClientError


LOCKOUT_AFTER = 5       # attempts
LOCKOUT_WINDOW = 900    # 15 minutes
TTL_BUFFER = 3600       # extra 1 hour


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

    # Check account locked state
    locked, remaining = is_locked_out(username)
    if locked:
        return _response(
            423,
            {
               "errorCode": "ACCOUNT_LOCKED",
               "message": "account locked due to too many failed attempts. please try again later.",
               "retryAfterSeconds": remaining,
            }
        )

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
            record_failed_attempt(username)
        elif code == "UserNotConfirmedException":
            status = 403
            message = "user is not confirmed"
        elif code == "PasswordResetRequiredException":
            status = 403
            message = "password reset required"
        elif code == "TooManyRequestsException":
            status = 429
            message = "too many attempts, please try again later"

        return status, {"errorCode": code, "message": message}

    auth = result.get("AuthenticationResult", {})
    return 200, {
        "accessToken": auth.get("AccessToken"),
        "idToken": auth.get("IdToken"),
        "refreshToken": auth.get("RefreshToken"),
    }


def record_failed_attempt(username: str):
    lockouts = get_lockouts_table()
    now = int(time.time())
    
    # Atomic counter increment
    resp = lockouts.update_item(
        Key={"username": username},
        UpdateExpression="SET attempts = if_not_exists(attempts, :start) + :inc, last_attempt = :now, ttl = :ttl",
        ExpressionAttributeValues={
            ":start": 0,
            ":inc": 1,
            ":now": now,
            ":ttl": now + LOCKOUT_WINDOW + TTL_BUFFER,
        },
        ReturnValues="UPDATED_NEW"
    )


def is_locked_out(username: str):
    lockouts = get_lockouts_table()
    now = int(time.time())
    resp = lockouts.get_item(Key={"username": username})
    item = resp.get("Item")
    if not item:
        return False, None

    attempts = int(item.get("attempts", 0))
    last_attempt = int(item.get("last_attempt", 0))

    if attempts < LOCKOUT_AFTER:
        return False, None

    unlock_at = last_attempt + LOCKOUT_WINDOW
    remaining = unlock_at - now
    if remaining > 0:
        return True, remaining

    return False, None


def get_lockouts_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ.get("LOCKOUT_TABLE_NAME", "Lockouts-dev"))
