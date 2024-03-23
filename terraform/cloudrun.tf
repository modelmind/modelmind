resource "google_cloud_run_v2_service" "cloud_run_api" {
  name     = local.api_cloud_run_name
  location = "europe-west1"
  # Only initial deployment
  lifecycle {
    ignore_changes = [
      template,
      client,
      client_version,
    ]
  }

  template {
    containers {
      image = "gcr.io/cloudrun/hello"
    }
  }
}

resource "google_service_account" "cloud_run_api_sa" {
  account_id   = local.api_cloud_run_name
  display_name = "Service Account for ${google_cloud_run_v2_service.cloud_run_api.name}"
  description  = "Service Account for ${google_cloud_run_v2_service.cloud_run_api.name}"
}

resource "google_service_account_iam_member" "service_account_iam_member_cloud_run_api_sa" {
  service_account_id = local.sa_cloudbuild_id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
}

resource "google_project_iam_member" "project_iam_member_sa" {
  for_each = toset([
    "roles/datastore.user",
    "roles/bigquery.user",
  ])
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
  project = var.project_id
}

resource "google_secret_manager_secret_iam_member" "binding_mm_jwt_secret_key" {
  secret_id = google_secret_manager_secret.mm_jwt_secret_key.name
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "binding_mm_sentry_dsn" {
  secret_id = google_secret_manager_secret.mm_sentry_dsn.name
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "binding_discord_notifications_webhook_id" {
  secret_id = google_secret_manager_secret.discord_notifications_webhook_id.name
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_api_sa.email}"
}
