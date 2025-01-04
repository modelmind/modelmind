env "local" {
  src = "file://schema.hcl"
  url = getenv("DATABASE_URL")
  dev = "docker://postgres/15/dev?search_path=public"
}
