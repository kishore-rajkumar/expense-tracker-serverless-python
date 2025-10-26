# Sprint 01 - Plan

## Sprint Overview

### Duration: 2 weeks

**Objective:** Implement user authentication feature (AWS Cognito signup/login) as the first functional MVP module.

### Sprint Goal
Deliver a fully functional authentication backend with endpoints for signup, login, and token-based identity validation using AWS Cognito integrated with API Gateway and Lambda.

## Epics and Issues

**Epic:** Authentication and User Management

**Linked Issues:**
- Setup Cognito User Pool and Identity Pool
- Implement Signup Lambda
- Implement Login Lambda
- Create Auth API Gateway Integration
- Test Authentication Flow Locally
- Configure IAM Roles and Policies for secure access

## Sprint Backlog

Issue  |  Task                                       |  Owner              |  Status  |  Priority
-------|---------------------------------------------|---------------------|----------|----------
#1     |  Setup Cognito User Pool and Identity Pool  |  @kishore-rajkumar  |  To Do   |  High    
#2     |  Implement Signup Lambda                    |  @kishore-rajkumar  |  To Do   |  High    
#3     |  Implement Login Lambda                     |  @kishore-rajkumar  |  To Do   |  Medium  
#4     |  Create Auth API Gateway Integration        |  @kishore-rajkumar  |  To Do   |  Medium  
#5     |  Test Authentication Flow Locally           |  @kishore-rajkumar  |  To Do   |  High    
#6     |  Configure IAM Roles and Policies           |  @kishore-rajkumar  |  To Do   |  High    


## Definition of Done (DoD)
- All authentication endpoints deployed via SAM CLI.
- Functional Cognito signup/login with proper IAM policies.
- Unit tests for all Lambdas (pytest).
- CI/CD pipeline passes without errors.
- Documentation updated under docs/.

## Sprint Metrics
- Velocity Target: Complete all 6 issues.
- Expected Deliverable: Deployed authentication module tested locally and via AWS.
- Sprint Review: Validate end-to-end auth flow, document findings, and create follow-up issues for next sprint (Expense CRUD).

## Retrospective (to be filled post-sprint)
- What went well
- What can be improved
- Action items for next sprint
