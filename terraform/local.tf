locals {
  app_name                    = "modelmind"
  github_owner                = "modelmind"
  github_repo_name            = "modelmind"
  tf_push_prod_trigger_name   = "${local.github_repo_name}-tf-on-push-prod"
  tf_pr_trigger_name          = "${local.github_repo_name}-tf-on-pr-prod"
  on_push_prod_api            = "deploy-${local.app_name}"
  api_cloud_run_name          = local.app_name
  internal_api_cloud_run_name = "${local.app_name}-internal"
  lb_ip_address_name          = "lb-${local.app_name}-ip-address"

  modelmind_zone_name = "modelmind-me"
  modelmind_dns_name  = "modelmind.me."
  subdomain_name      = "api"
  domain_name         = "${local.subdomain_name}.modelmind.me"
  http_lb_name        = "${local.app_name}-lb"

  # -- remote vars --
  sa_cloudbuild_id = data.terraform_remote_state.infra_remote_state.outputs.persony_sa_cloud_build_id
  log_bucket_name  = data.terraform_remote_state.infra_remote_state.outputs.persony_log_bucket_name
  sa_infra         = data.terraform_remote_state.infra_remote_state.outputs.persony_sa_infra
}
