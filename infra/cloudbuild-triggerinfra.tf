resource "google_cloudbuild_trigger" "tf-pr" {
  name            = local.tf_pr_trigger_name
  description     = "Make a terraform plan on pr"
  location        = "europe-west1"
  ignored_files   = ["README.md", ".gitignore"]
  filename        = "terraform/tf_pr_cloudbuild.yml"
  included_files  = ["terraform/**"]
  service_account = local.sa_infra.id
  github {
    owner = local.github_owner
    name  = local.github_repo_name
    pull_request {
      branch = "^main$"
    }
  }
  substitutions = {
    "_LOGS_GCS_BUCKET" : "${local.log_bucket_name}/${local.on_push_prod_api}"
  }
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
}
