
# AWS Foundations Notes

Author: Shad0w2
Project: CloudMart ERP Platform
Phase: AWS Foundations
Date: 2026-05-26

---

# 1. AWS Account Information

## AWS Account Type
Personal Learning Account

## Root Account Security Status
- MFA Enabled: YES
- Root user used for daily tasks: NO

## Default Region
ap-south-1 (Mumbai)

Reason:
- Closest AWS region
- Lower latency for India
- Good for learning and deployment

---

# 2. IAM Setup

## IAM Admin User

Username:
cloud-admin

Purpose:
Administrative account for daily AWS operations.

## Permissions Attached

Policy:
AdministratorAccess

## Why IAM Users Are Important

Best practice:
- Never use root account daily
- Use IAM users with limited permissions
- Apply least privilege principle

## Authentication Method

- Password login enabled
- MFA enabled (recommended)

---

# 3. MFA Configuration

## MFA Application Used

Example:
Google Authenticator

## Why MFA Is Important

MFA protects the AWS account even if:
- Password is leaked
- Credentials are stolen
- Phishing occurs

## AWS Security Best Practice

Always enable MFA for:
- Root account
- Admin IAM users

---

# 4. Billing Alerts

## Billing Alarm Thresholds

| Threshold | Purpose |
|---|---|
| $5 | Early warning |
| $10 | Immediate review |

## Service Used

- CloudWatch
- SNS

## Notification Method

Email notifications enabled.

## Importance

Billing alarms help prevent:
- Unexpected costs
- Forgotten running resources
- Accidental expensive deployments

---

# 5. AWS CLI Setup

## Installed Version

Command:
```bash
aws --version
````

Example Output:

```text
aws-cli/2.x.x Python/3.x Windows/10 exe/AMD64
```

---

## AWS CLI Configuration

Command:

```bash
aws configure
```

Configured Values:

| Setting | Value      |
| ------- | ---------- |
| Region  | ap-south-1 |
| Output  | json       |

---

## Credential File Location

### Windows

```text
C:\\Users\\<username>\\.aws\\credentials
```

### Linux/macOS

```text
~/.aws/credentials
```

---

## Important AWS CLI Commands

### Verify identity

```bash
aws sts get-caller-identity
```

### List S3 buckets

```bash
aws s3 ls
```

### List EC2 instances

```bash
aws ec2 describe-instances
```

### Configure CLI again

```bash
aws configure
```

---

# 6. Git Setup

## Installed Version

Command:

```bash
git --version
```

---

## Git Global Configuration

Commands:

```bash
git config --global user.name \"Your Name\"
git config --global user.email \"your-email@example.com\"
```

---

## Why Git Is Important

Git provides:

* Version control
* Collaboration
* Rollback capability
* Change tracking

Used heavily in:

* DevOps
* Cloud engineering
* CI/CD pipelines

---

# 7. VS Code Setup

## Installed Extensions

| Extension   | Purpose                |
| ----------- | ---------------------- |
| AWS Toolkit | AWS integration        |
| Python      | Backend development    |
| Docker      | Container management   |
| Terraform   | Infrastructure as Code |

---

## Why VS Code Is Used

* Lightweight
* Strong extension ecosystem
* Terminal integration
* Git integration
* Infrastructure editing support

---

# 8. AWS Regions & Availability Zones

## Region Definition

A region is a geographic location containing AWS infrastructure.

Example:

* ap-south-1 (Mumbai)
* us-east-1 (Virginia)

---

## Availability Zone Definition

Availability Zones are isolated datacenters within a region.

Example:

* ap-south-1a
* ap-south-1b

---

## Why Multiple AZs Matter

Using multiple AZs improves:

* High availability
* Fault tolerance
* Disaster resilience

---

# 9. Shared Responsibility Model

## AWS Responsibilities

AWS manages:

* Physical datacenters
* Hardware
* Networking infrastructure
* Managed service infrastructure

---

## Customer Responsibilities

Customer manages:

* IAM permissions
* EC2 operating system
* Security groups
* Application security
* Data encryption

---

## Important Understanding

Cloud security is shared.

AWS secures the cloud.
Customer secures resources inside the cloud.

---

# 10. Project Repository Structure

```text
cloudmart-project/
│
├── docs/
├── diagrams/
├── terraform/
├── backend/
├── frontend/
└── scripts/
```

---

## Folder Purposes

### docs/

Documentation and architecture notes.

### diagrams/

Network diagrams and architecture drawings.

### terraform/

Infrastructure as Code templates.

### backend/

Backend application code.

### frontend/

Frontend UI application.

### scripts/

Automation scripts.

---

# 11. Important Learnings

## Key Concepts Learned

* IAM basics
* MFA importance
* AWS CLI setup
* Billing monitoring
* Regions vs AZs
* Shared responsibility model

---

# 12. Common Troubleshooting

## AWS CLI Not Working

### Problem

```text
aws command not found
```

### Solution

Reinstall AWS CLI and verify PATH variable.

---

## Invalid Credentials

### Problem

```text
Unable to locate credentials
```

### Solution

Run:

```bash
aws configure
```

---

## Permission Denied Errors

### Possible Cause

IAM user missing permissions.

### Solution

Verify IAM policies attached.

---

# 13. Future Improvements

Planned next steps:

* Create custom VPC
* Configure public/private subnets
* Configure EC2 instances
* Deploy ERP application

---

# 14. References

## AWS Official Documentation

AWS CLI:
[https://docs.aws.amazon.com/cli/](https://docs.aws.amazon.com/cli/)

IAM:
[https://docs.aws.amazon.com/IAM/](https://docs.aws.amazon.com/IAM/)

CloudWatch:
[https://docs.aws.amazon.com/cloudwatch/](https://docs.aws.amazon.com/cloudwatch/)

---

# 15. Personal Notes

(Add your own observations and mistakes here)

Example:

* Learned difference between root and IAM user.
* Understood why MFA is critical.
* AWS CLI configuration initially failed due to wrong access key.

```

---

# Why This Documentation Matters

This single file helps you:
- Build professional documentation habits
- Understand concepts deeply
- Prepare for interviews
- Track mistakes and learnings
- Build real DevOps discipline

In actual cloud teams:
- Engineers document everything
- Good documentation reduces outages
- Documentation speeds onboarding
- Documentation becomes operational knowledge

---

# Pro Tip

As we continue phases:
- Add screenshots
- Add architecture diagrams
- Add commands you used
- Add errors and fixes
- Add cost observations
- Add security notes

By the end, this becomes a complete cloud engineering knowledge base for your project.
```
