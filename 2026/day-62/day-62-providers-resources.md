Day 62 — Terraform Providers, Resources, and Dependencies

Building a complete AWS networking stack and understanding how Terraform determines resource creation order.

**Task 1: Exploring the AWS Provider**

I began by initializing a new Terraform project and configuring the AWS provider.

Running terraform init downloaded the required provider plugin (hashicorp/aws v5.0.0) and verified it using HashiCorp’s signature system.

What is .terraform.lock.hcl?

The lock file captures the exact provider version and checksums selected during initialization. This guarantees that every team member — and any CI/CD pipeline — uses the same provider binary.

This consistency prevents unexpected behavior caused by version drift and is why the lock file should always be committed to version control.

Version Constraint Comparison
Constraint	Meaning
~> 5.0	Allows only 5.x versions (e.g., 5.1, 5.9)
>= 5.0	Allows any version 5.0 or higher (including future major versions)
= 5.0.0	Pins to exactly version 5.0.0

Using ~> 5.0 is a safe production default — it permits minor updates and bug fixes without introducing breaking changes.

**Task 2: Building a VPC from Scratch**

I defined a complete AWS networking stack consisting of:

A VPC as the root network container
A subnet for hosting resources
An internet gateway for external connectivity
A route table to direct traffic
A route table association linking the subnet and routing rules

Running terraform plan confirmed:

Plan: 5 to add, 0 to change, 0 to destroy

After applying, all resources were successfully created and visible in the AWS console:

**Task 3: Understanding Implicit Dependencies**

Terraform automatically determines the correct order of resource creation using implicit dependencies.

How it works

When one resource references another (e.g., a subnet referencing a VPC ID), Terraform:

Detects the reference
Builds a dependency graph (DAG — Directed Acyclic Graph)
Orders operations using topological sorting

This ensures resources are created in the correct sequence without manual intervention.

What if ordering was wrong?

If a subnet were created before its VPC, the operation would fail because the required VPC ID would not exist. Terraform avoids this by resolving dependencies before making API calls.

Key dependencies in this setup
Subnet depends on VPC
Internet Gateway depends on VPC
Route Table depends on both VPC and Internet Gateway
Route Table Association depends on Subnet and Route Table
**Task 4: Adding a Security Group and EC2 Instance**

Next, I extended the infrastructure with:

A security group allowing SSH (22) and HTTP (80) access
An EC2 instance deployed inside the subnet

The instance launched successfully with a public IP inside the custom VPC:

**Task 5: Explicit Dependencies with depends_on**

Not all dependencies are automatically detected.

I added an S3 bucket intended for application logs. Since it didn’t directly reference the EC2 instance, Terraform wouldn’t naturally enforce ordering.

To ensure correct sequencing, I used an explicit dependency.

Dependency Graph

Terraform generates a full dependency graph of all resources, which can be visualized:

When to use explicit dependencies

Use depends_on when:

IAM propagation delays
Policies may not be immediately usable after creation, affecting dependent services.
Resource access sequencing
Example: ensuring permissions (like S3 bucket policies) exist before a service attempts access.
**Task 6: Lifecycle Rules and Destroy Behavior**
create_before_destroy

This lifecycle rule ensures that when a resource must be replaced, the new version is created before the old one is removed — minimizing downtime.


Destroy Order

Terraform destroys resources in reverse dependency order:

Child resources are deleted first
Parent resources are deleted last

This prevents dependency violations during teardown.

All resources were removed cleanly.

Lifecycle Arguments Overview
Argument	Purpose	Use Case
create_before_destroy	Replace resources without downtime	Critical infrastructure like EC2 or databases
prevent_destroy	Blocks accidental deletion	Production data resources
ignore_changes	Ignores drift in specific attributes	When external systems modify resources
Implicit vs Explicit Dependencies — Summary

Implicit dependencies are automatically inferred when resources reference each other. They cover most real-world scenarios and allow Terraform to build and execute a dependency graph efficiently.

Explicit dependencies (depends_on) are required when relationships exist outside Terraform’s expression graph — typically due to runtime behavior rather than configuration references.

**Key Takeaway**

Terraform is not a linear execution tool — it is a graph-based engine.

It:

Builds a dependency graph
Executes independent resources in parallel
Ensures correct ordering automatically
Destroys infrastructure safely in reverse order

This graph-driven model is what makes Terraform reliable, scalable, and production-ready.