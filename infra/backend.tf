terraform {
  backend "gcs" {
    bucket = "persony-logs-f55705bfe7afb2896b12bc430093695c"
    prefix = "persony"
  }
}
