# GCP Infrastructure for VigilantiAI

This directory contains Terraform configuration to provision the Google Cloud Platform infrastructure required for the VigilantiAI system.

## Resources Provisioned
*   **VPC Network**: Custom VPC with public and private subnets.
*   **Cloud NAT**: Enables internet access for private GKE nodes.
*   **GKE Cluster**: Regional/Zonal Kubernetes cluster with autoscaling enabled.
*   **Artifact Registry**: Docker repository for storing application images.

## Prerequisites
1.  [Install Terraform](https://developer.hashicorp.com/terraform/downloads)
2.  [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3.  Authenticate with GCP:
    ```bash
    gcloud auth application-default login
    ```

## Usage

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

2.  **Create `terraform.tfvars`**:
    Create a file named `terraform.tfvars` with your project details:
    ```hcl
    project_id = "your-gcp-project-id"
    region     = "us-central1"
    ```

3.  **Plan**:
    Review the changes to be applied.
    ```bash
    terraform plan
    ```

4.  **Apply**:
    Provision the resources.
    ```bash
    terraform apply
    ```

## Outputs
After a successful apply, Terraform will output:
*   `cluster_name`: Name of the created GKE cluster.
*   `cluster_endpoint`: The IP address of the cluster master.
*   `repository_url`: The URL of the created Artifact Registry repository.
