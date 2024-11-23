terraform {
  required_version = "~> 1.8.1"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.26"
    }
  }
}


provider "google" {
  project = var.project_id
}
