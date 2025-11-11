import json
import re


def validate_email(email):
    """
    Validate the email format using a regex pattern.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if email format is valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate the password format.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if password criteria is met, False otherwise.
    """
    return password is not None and len(password) >= 8


def lambda_handler(event, context):
    """
    AWS Lambda handler function to process user registration.

    Args:
        event (dict): The event payload containing request data.
        context (object): Lambda context object (not used here).

    Returns:
        dict: API Gateway compatible HTTP response with status and message.
    """

    # Parse JSON body safely from event
    body = json.loads(event.get('body') or '{}')
    email = body.get('email')
    password = body.get('password')
    name = body.get('name')

    # Validate email presence and format
    if not email or not validate_email(email):
        return response(400, {'message': 'Invalid or missing email.'})

    # Validate password criteria
    if not validate_password(password):
        return response(400, {'message': 'Password does not meet criteria.'})

    # Validate name presence
    if not name:
        return response(400, {'message': 'Name is required.'})

    # Return success response for now
    return response(201, {"message": "User registered successfully"})


def response(status_code, body):
    """
    Construct a standard HTTP response for API Gateway.

    Args:
        status_code (int): HTTP status code.
        body (dict): Response body as a dictionary.

    Returns:
        dict: Formatted response with status code, JSON body, and headers.
    """

    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }
