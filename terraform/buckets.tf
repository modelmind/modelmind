resource "google_storage_bucket" "modelmind_results_exports" {
  name          = "modelmind-results-exports"
  location      = "europe-west1"
  storage_class = "STANDARD"

  cors {
    origin          = ["https://*.${local.rootdomain_name}"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }

  public_access_prevention = "enforced"

}
