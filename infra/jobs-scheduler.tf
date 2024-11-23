resource "google_service_account" "modelmind_scheduler_sa" {
  account_id   = "${local.api_cloud_run_name}-scheduler"
  display_name = "Service Account for ${google_cloud_run_v2_service.cloud_run_api.name} scheduler"
  description  = "Service Account for ${google_cloud_run_v2_service.cloud_run_api.name} scheduler"
}

resource "google_cloud_run_v2_job" "schedule_calculate_persony_statistics_tasks" {
  name     = "schedule-calculate-persony-statistics-tasks"
  location = "europe-west1"
  template {
    template {
      containers {
        image = "gcr.io/cloudrun/hello"
      }
    }
  }
}

resource "google_cloud_scheduler_job" "schedule_calculate_persony_statistics_tasks" {
  provider         = google-beta
  name             = "schedule-calculate-persony-statistics-tasks"
  description      = "Schedule calculate persony statistics tasks"
  schedule         = "00 9 * * *"
  attempt_deadline = "60s"
  region           = "europe-west1"
  project          = var.project_id

  retry_config {
    retry_count = 0
  }

  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_number}/jobs/${google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.name}:run"

    oauth_token {
      service_account_email = google_service_account.modelmind_scheduler_sa.email
    }
  }
}

resource "google_cloud_run_v2_job_iam_member" "schedule_calculate_persony_statistics_tasks" {
  project  = var.project_id
  name     = google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.name
  location = google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.modelmind_scheduler_sa.email}"
}
