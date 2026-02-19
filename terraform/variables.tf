variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
  default     = "vigilantiai-cluster"
}

variable "repository_name" {
  description = "The name of the Artifact Registry repository"
  type        = string
  default     = "vigilantiai-repo"
}
