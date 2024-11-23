resource "google_cloud_tasks_queue" "calculate_questionnaire_statistics" {
  name     = "calculate-questionnaire-statistics"
  location = "europe-west1"

  rate_limits {
    max_concurrent_dispatches = 10
    max_dispatches_per_second = 1
  }

  retry_config {
    max_attempts = 1
  }
}

resource "google_cloud_tasks_queue_iam_member" "calculate_questionnaire_statistics" {
  for_each = toset([
    "roles/cloudtasks.admin",
    "roles/cloudtasks.queueAdmin"
  ])
  role     = each.key
  project  = var.project_id
  location = google_cloud_tasks_queue.calculate_questionnaire_statistics.location
  name     = google_cloud_tasks_queue.calculate_questionnaire_statistics.name
  member   = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
}
