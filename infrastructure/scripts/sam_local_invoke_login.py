#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

STACK_NAME = "expense-tracker-dev"      # adjust
FUNCTION_NAME = "LoginFunction"         # logical name in template
REGION = "us-east-1"                    # adjust if needed

TEMPLATE_PATH = "infrastructure/template.yaml"
EVENT_PATH = "infrastructure/events/login_success.json"
ENV_PATH = "infrastructure/env.local.json"


def aws_cli(args):
    cmd = ["aws"] + args
    try:
        out = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR running: {' '.join(cmd)}", file=sys.stderr)
        print(e.output, file=sys.stderr)
        sys.exit(1)
    return out.strip()


def get_client_id():
    client_id = aws_cli([
        "cloudformation", "describe-stack-resources",
        "--stack-name", STACK_NAME,
        "--logical-resource-id", "ExpenseTrackerUserPoolClient",
        "--query", "StackResources[0].PhysicalResourceId",
        "--output", "text",
        "--region", REGION,
    ])
    if not client_id:
        print("No ClientId returned. Check STACK_NAME and logical resource id.", file=sys.stderr)
        sys.exit(1)
    return client_id


def write_env_file(client_id: str):
    env = {
        FUNCTION_NAME: {
            "COGNITO_CLIENT_ID": client_id,
            "AWS_REGION": REGION,
        }
    }
    path = Path(ENV_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(env, indent=2))
    print(f"Wrote {path} with COGNITO_CLIENT_ID={client_id}")


# def sam_local_invoke():
#     cmd = [
#         "sam", "local", "invoke", FUNCTION_NAME,
#         "-t", TEMPLATE_PATH,
#         "-e", EVENT_PATH,
#         "--env-vars", ENV_PATH,
#         "--region", REGION,
#     ]
#     print("Running:", " ".join(cmd))
#     # stream output directly
#     subprocess.check_call(cmd)

def sam_local_invoke():
    cmd_str = (
        f"sam local invoke {FUNCTION_NAME} "
        f"-t {TEMPLATE_PATH} "
        f"-e {EVENT_PATH} "
        f"--env-vars {ENV_PATH} "
        f"--region {REGION}"
    )
    print("Running:", cmd_str)
    # Use shell=True so PowerShell/CMD resolves 'sam' the same way as your prompt
    subprocess.check_call(cmd_str, shell=True)


def main():
    client_id = get_client_id()
    write_env_file(client_id)
    sam_local_invoke()


if __name__ == "__main__":
    main()
