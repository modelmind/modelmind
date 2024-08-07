resource "google_cloudbuild_trigger" "on-push-prod-api" {
  name            = local.on_push_prod_api
  description     = "Deploy ${local.app_name} api"
  location        = "europe-west1"
  ignored_files   = ["terraform/**"]
  filename        = "deploy_cloud_run_prod.yml"
  service_account = local.sa_cloudbuild_id
  github {
    owner = local.github_owner
    name  = local.github_repo_name
    push {
      branch = "^main$"
    }
  }
  substitutions = {
    "_APP_NAME" : local.app_name
    "_PROJECT_ID" : var.project_id
    "_DOMAIN" : local.domain_name
    "_LOGS_GCS_BUCKET" : "${local.log_bucket_name}/${local.on_push_prod_api}"
    "_TARGET_SERVICE_IMAGE" : "europe-docker.pkg.dev/${var.project_id}/docker/${local.app_name}-api"
    "_SERVICE_NAME" : google_cloud_run_v2_service.cloud_run_api.name
    "_INTERNAL_SERVICE_NAME" : google_cloud_run_v2_service.internal_cloud_run_api.name
    "_REGION" : "europe-west1"
    "_DOCKER_IMAGE" : "gcr.io/cloud-builders/docker:latest"
    "_PYTHON_IMAGE_SLIM" : "python:3.11-slim"
    "_CLOUD_SDK_IMAGE" : "gcr.io/google.com/cloudsdktool/cloud-sdk:latest"
    "_FIREBASE_IMAGE" : "gcr.io/${var.project_id}/firebase"
    "_PORT" : "8080"
    "_CLOUDRUN_TAG" : "prod"
    "_SERVER__LOG_LEVEL" : "info"
    "_ENVIRONMENT" : "prod"
    "_FIRESTORE__DATABASE" : "(default)"
    "_SENTRY__DSN" : "${google_secret_manager_secret.mm_sentry_dsn.name}:latest"
    "_JWT__SECRET_KEY" : "${google_secret_manager_secret.mm_jwt_secret_key.name}:latest"
    "_JWT__NEXT_SECRET" : "${google_secret_manager_secret.mm_jwt_next_secret.name}:latest"
    "_DISCORD__NOTIFICATIONS_WEBHOOK_ID" : "${google_secret_manager_secret.discord_notifications_webhook_id.name}:latest"
    "_TASKS_QUEUE_CALCULATE_STATISTICS__PROJECT" : "${google_cloud_tasks_queue.calculate_questionnaire_statistics.project}"
    "_TASKS_QUEUE_CALCULATE_STATISTICS__LOCATION" : "${google_cloud_tasks_queue.calculate_questionnaire_statistics.location}"
    "_TASKS_QUEUE_CALCULATE_STATISTICS__QUEUE" : "${google_cloud_tasks_queue.calculate_questionnaire_statistics.name}"
    "_JOBS_SCHEDULE_CALCULATE_STATISTICS_TASKS__NAME" : "${google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.name}"
    "_JOBS_SCHEDULE_CALCULATE_STATISTICS_TASKS__LOCATION" : "${google_cloud_run_v2_job.schedule_calculate_persony_statistics_tasks.location}"
    "_SA_EMAIL" : google_service_account.cloud_run_api_sa.email
  }
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
}
