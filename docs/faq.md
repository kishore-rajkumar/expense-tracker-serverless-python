# Frequently Asked Questions (FAQ)

---

## How do I configure AWS credentials for local development?

Use the AWS CLI:
```
aws configure
```

Enter your Access Key ID, Secret Access Key, region, and output format.  
See [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for help.

---

## Why does the CI/CD workflow fail?

Common reasons:
- Linting errors (`flake8`)
- Tests fail (`pytest`)
- Incorrect branch naming or PR checklist incomplete
- Missing or incorrect environment variables

Check the Actions tab for detailed error logs, and see [`docs/ci-cd-pipeline.md`](./ci-cd-pipeline.md).

---

## How do I run tests locally?
```
pytest
flake8 .
```
Make sure dependencies (`requirements.txt`) are installed.

---

## How do I deploy my changes?

Use AWS SAM CLI for deployment:
```
sam build
sam deploy --guided
```

Follow the prompts and ensure your AWS credentials are configured.

---

## Who do I contact for questions or issues?

- Open an [Issue](https://github.com/kishore-rajkumar/expense-tracker-serverless-python/issues)
- Tag a maintainer in your issue or discussion

---

## Where can I find architecture and execution documentation?

- [`docs/architecture.md`](./architecture.md)
- [`docs/project-execution-steps-order.md`](./project-execution-steps-order.md)

---
