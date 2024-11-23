data "terraform_remote_state" "infra_remote_state" {
  backend   = "gcs"
  workspace = terraform.workspace
  config = {
    bucket = "modelmind-terraform-infra-state"
    prefix = "tf"
  }
}
