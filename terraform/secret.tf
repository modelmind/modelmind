resource "random_password" "mm_jwt_secret_key_value" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "google_secret_manager_secret" "mm_jwt_secret_key" {
  secret_id = "mm_jwt_secret_key"

  replication {
    user_managed {
      replicas {
        location = "europe-west1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "mm_jwt_secret_key_version" {
  secret      = google_secret_manager_secret.mm_jwt_secret_key.id
  secret_data = random_password.mm_jwt_secret_key_value.result
}

resource "google_secret_manager_secret" "mm_sentry_dsn" {
  secret_id = "mm_sentry_dsn"

  replication {
    user_managed {
      replicas {
        location = "europe-west1"
      }
    }
  }
}

resource "google_secret_manager_secret" "discord_notifications_webhook_url" {
  secret_id = "discord_notifications_webhook_url"

  replication {
    user_managed {
      replicas {
        location = "europe-west1"
      }
    }
  }
}
