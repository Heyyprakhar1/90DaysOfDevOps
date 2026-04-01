# Day 61 — Introduction to Terraform and Your First AWS Infrastructure

## What is Infrastructure as Code (IaC)?

Infrastructure as Code means defining your cloud resources — servers, networks, storage buckets — using code files instead of clicking around in a UI. Think of it like writing a recipe: instead of cooking something differently every time, you write down exact steps so anyone (or any machine) can reproduce the same result. In DevOps, this matters because infrastructure that lives only in someone's memory or in a series of console clicks is fragile, hard to reproduce, and impossible to review or version-control. IaC makes your infrastructure auditable, repeatable, and automatable — the same way application code is.

---

## What Problems Does IaC Solve?

When you create resources manually through the AWS console, there is no record of *what* you clicked or *why*. A few problems this causes:

- **No reproducibility** — you can't spin up the exact same environment in a different region or account without repeating every step manually.
- **Drift** — over time, different team members make small changes in the console and your environment silently diverges from what you think it is.
- **No peer review** — you can't open a Pull Request for clicking buttons.
- **Slow recovery** — if something breaks, recreating it from memory is risky and slow.

IaC fixes all of this: your infrastructure is in a `.tf` file, tracked in Git, reviewable, and can be rebuilt from scratch in minutes.

---

## Terraform vs Other IaC Tools

| Tool | Key Difference |
|---|---|
| **AWS CloudFormation** | AWS-only, uses JSON/YAML, tightly integrated with AWS services but no support for other clouds |
| **Ansible** | Primarily a configuration management tool (installs software, manages OS settings) — not designed for provisioning cloud resources from scratch |
| **Pulumi** | Uses real programming languages (Python, TypeScript, Go) — powerful but requires coding knowledge; Terraform uses its own simpler HCL language |
| **Terraform** | Cloud-agnostic, declarative, large community, works across AWS, GCP, Azure, and more |

---

## What Does "Declarative" and "Cloud-Agnostic" Mean?

**Declarative** means you describe the *end state* you want, not the *steps* to get there. You tell Terraform "I want an S3 bucket named X" — and it figures out how to create it, what API calls to make, and what order to do things in. You don't write a script that says "call CreateBucket, then wait, then tag it." You just say what you want.

**Cloud-agnostic** means Terraform works with many cloud providers — AWS, Azure, Google Cloud, and others — using the same workflow and the same HCL syntax. You change the *provider*, not the entire toolchain.

---

## Task 2: Setup — Terraform & AWS CLI

Verified Terraform v1.14.8 installed on Linux (WSL2/Ubuntu), AWS CLI v2.28.21 configured, and AWS credentials validated using `aws sts get-caller-identity` — confirming the IAM user `terra-for-practice` under account `373515081834`.

![Terraform version and AWS CLI configured](screenshots/Screenshot_2026-04-01_130719.png)

---

## Task 3: Creating an S3 Bucket with Terraform

### The `main.tf` Config

Wrote the config using `vim`, ran `terraform fmt` to auto-format, and `terraform validate` to confirm the syntax was correct before running any commands. The provider was set to `eu-west-1` (Ireland) with the `hashicorp/aws` provider version `6.38.0`.

![main.tf content and terraform init output](screenshots/Screenshot_2026-04-01_131716.png)

### What `terraform init` Downloaded

`terraform init` read the `required_providers` block and downloaded the `hashicorp/aws` provider plugin (v6.38.0) into the `.terraform/` directory. It also created a `.terraform.lock.hcl` file to lock the exact provider version — ensuring anyone else running this config gets the same provider binary.

The `.terraform/` directory contains:
- The provider plugin binary (the actual code that knows how to talk to AWS APIs)
- A `providers/` subdirectory with the versioned plugin
- The lock file ensuring reproducible provider versions

### `terraform apply` — Bucket Created

![terraform apply creating S3 bucket and aws s3 ls confirmation](screenshots/Screenshot_2026-04-01_132627.png)

The bucket `tws-terraweek-bucket` was created in 6 seconds. Confirmed with `aws s3 ls` — the bucket appeared with timestamp `2026-04-01 07:55:43`.

### S3 Bucket in the AWS Console

![S3 bucket visible in AWS console in eu-west-1](screenshots/Screenshot_2026-04-01_133112.png)

The bucket `tws-terraweek-bucket` is visible in the S3 console under the `eu-west-1 (Europe Ireland)` region, created on April 1, 2026.

---

## Task 4: Adding an EC2 Instance

Added an `aws_instance` resource to `main.tf` — AMI `ami-083533119a217b3a6` (Amazon Linux 2 for `eu-west-1`), instance type `t2.micro`, with tag `Name = "TerraWeek-Day1"`.

### `terraform plan` — Only EC2 to Add

When running `terraform plan` after the bucket already existed, Terraform refreshed the S3 bucket state (confirming it already exists) and only planned to **create** the EC2 instance — 1 resource to add, 0 to change, 0 to destroy.

![terraform plan showing only EC2 instance to be created](screenshots/Screenshot_2026-04-01_134702.png)

### How Does Terraform Know the Bucket Already Exists?

Terraform doesn't scan your AWS account to check what's there. It compares your `main.tf` (desired state) against the `terraform.tfstate` file (what it already created and recorded). The S3 bucket was already in the state file from the previous apply, so Terraform only planned to add the missing EC2 instance.

### `terraform apply` — EC2 Instance Created

![terraform apply creating EC2 and console showing instance running with TerraWeek-Day1 tag](screenshots/Screenshot_2026-04-01_134732.png)

The EC2 instance `i-0f52520e7ff1111e1` was created after 38 seconds and is visible in the AWS console (eu-west-1) with instance state **Running** and the tag `TerraWeek-Day1`.

---

## Task 5: Exploring the State File

### `terraform state show aws_s3_bucket.my_bucket`

![terraform state show for the S3 bucket](screenshots/Screenshot_2026-04-01_135230.png)

The state file stores every attribute of the resource — the bucket ARN, region, domain name, encryption config, versioning config, ownership, and ACL grants. This is the full picture of what Terraform knows about the resource.

### `terraform state show aws_instance.my_instance`

![terraform state show for the EC2 instance](screenshots/Screenshot_2026-04-01_135436.png)

The EC2 state includes the instance ID, AMI, instance type, public/private IPs, subnet ID, security groups, availability zone, tags, and dozens of other attributes — everything needed to manage or recreate this resource.

### What Does the State File Store?

For every resource, the state file records:
- The **resource type and logical name** used in the config
- The **real-world ID** AWS assigned (e.g., `i-0f52520e7ff1111e1`)
- **All attributes** of the resource at the time of last apply
- **Dependencies** between resources

### Why You Should Never Manually Edit the State File

The state file is Terraform's source of truth. If you manually change an ID or attribute, Terraform's map to the real AWS resource breaks — it may try to create duplicate resources, fail to destroy existing ones, or lose track of IDs entirely. Always use `terraform state` commands if you need to manipulate state.

### Why the State File Should Not Be in Git

The state file can contain sensitive data — resource IDs, IP addresses, and sometimes even secrets. Beyond security, if two people commit conflicting state files, Terraform's tracking breaks completely. The correct approach is to store state remotely (e.g., in an S3 bucket with DynamoDB locking for state locking) rather than committing it locally.

---

## Task 6: Modify, Plan, and Destroy

### Tag Change — `terraform plan`

Updated the EC2 tag from `"TerraWeek-Day1"` to `"TerraWeek-Modified"` in `main.tf` and ran `terraform plan`.

![terraform plan showing in-place tag update](screenshots/Screenshot_2026-04-01_135914.png)

The plan showed `~ update in-place` with the change clearly displayed as `"TerraWeek-Day1" -> "TerraWeek-Modified"`. Plan: 0 to add, **1 to change**, 0 to destroy.

This is an **in-place update** — AWS can update tags without touching the underlying instance, so Terraform modifies it without destroying and recreating it.

### `terraform apply -auto-approve` — Tag Updated

![terraform apply confirming tag modification](screenshots/Screenshot_2026-04-01_140152.png)

Modification completed in 4 seconds. Resources: 0 added, **1 changed**, 0 destroyed.

### Tag Verified in AWS Console

![AWS console showing instance name updated to TerraWeek-Modified](screenshots/Screenshot_2026-04-01_140243.png)

![Side-by-side terminal and console showing TerraWeek-Modified instance running](screenshots/Screenshot_2026-04-01_140258.png)

The instance title in the AWS EC2 console updated to `TerraWeek-Modified` immediately after apply.

### `terraform destroy` — Everything Removed

![terraform destroy output showing 2 resources destroyed](screenshots/Screenshot_2026-04-01_140601.png)

Both the S3 bucket and EC2 instance were destroyed. The S3 bucket was gone in 2 seconds; the EC2 instance took 43 seconds to terminate. Resources: **2 destroyed**.

### Verified in AWS Console — Instance Terminated

![EC2 console showing TerraWeek-Modified instance in Terminated state](screenshots/Screenshot_2026-04-01_140700.png)

The EC2 instance `i-0f52520e7ff1111e1` (TerraWeek-Modified) shows **Terminated** status in the AWS console. The S3 bucket was also removed from the console.

---

## Key Terraform Commands — Quick Reference

| Command | What It Does |
|---|---|
| `terraform init` | Downloads providers and initializes the working directory |
| `terraform plan` | Shows a preview of changes without applying them |
| `terraform apply` | Creates or updates resources to match your config |
| `terraform destroy` | Destroys all resources managed by the current config |
| `terraform show` | Displays current state in a human-readable format |
| `terraform state list` | Lists all resources Terraform is currently tracking |
| `terraform state show <resource>` | Shows all attributes of a specific tracked resource |
| `terraform fmt` | Auto-formats your `.tf` files to standard style |
| `terraform validate` | Checks for syntax errors without connecting to AWS |

### Plan Symbols Explained

| Symbol | Meaning |
|---|---|
| `+` | Resource will be **created** |
| `-` | Resource will be **destroyed** |
| `~` | Resource will be **updated in-place** |
| `-/+` | Resource will be **destroyed and recreated** |

---

## .gitignore for Terraform Projects

```
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
```

---

*Day 61 of 90 Days of DevOps — TerraWeek Challenge*