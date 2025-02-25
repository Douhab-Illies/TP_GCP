terraform {
  backend "gcs" {
    bucket  =  ${var.SAVE_BUCKET} # Remplace par le nom de ton bucket
    prefix  = "terraform/state"      # Stocke le tfstate dans un sous-dossier
  }
}
