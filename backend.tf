terraform {
  backend "gcs" {
    bucket  =  "${var.SAVE_BUCKET}"
    prefix  = "terraform/state"
  }
}
