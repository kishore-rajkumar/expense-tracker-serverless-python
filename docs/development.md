# Local Development Environment Setup

## 1. Purpose

Set up a Python virtual environment for consistent dependency management across Linux, Windows, and SAM local testing. This ensures reproducible builds for your expense-tracker-serverless-python project.

## 2. Prerequisites

### Ubuntu/Debian
`sudo apt update && sudo apt install python3 python3-pip python3-venv`

### Verify versions (Python 3.9+ recommended for SAM)
```
python3 --version
pip3 --version
```

## 3. Create Virtual Environment

Navigate to project root and create isolated environment:

### Linux/macOS
`python3 -m venv .venv`

### Windows (Command Prompt/PowerShell)
`python -m venv .venv`


## 4. Activate Environment

### Linux/macOS
`source .venv/bin/activate`

### Windows Command Prompt
`.venv\Scripts\activate.bat`

### Windows PowerShell
`.venv\Scripts\Activate.ps1`


_Your prompt shows (.venv) when active._

## 5. Install Dependencies
```
pip install -r requirements.txt
pip install -e .  # For development (if setup.py exists)
```

## 6. SAM Development Workflow

### Build and test locally
```
sam build --use-container
sam local start-api
```

### Run in new terminal with venv active
`pytest tests/ -v`

## 7. Deactivate and Cleanup
```deactivate  # Exit virtual environment
rm -rf .venv  # Optional: remove when switching projects 
```

**Note:** Add .venv/ to .gitignore. For CI/CD, GitHub Actions handles dependencies via requirements.txt without local venv.
