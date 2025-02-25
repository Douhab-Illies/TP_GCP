# Création du bucket Cloud Storage
resource "google_storage_bucket" "sto_illies" {
  name          = var.BUCKET
  location      = var.REGION
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 5
    }
  }
}


# Création du Service Account
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}

# Attribution des droits IAM au Service Account
resource "google_project_iam_binding" "cloud_run_access" {
  project = var.ID
  role    = "roles/storage.objectViewer"
  members = ["serviceAccount:${google_service_account.cloud_run_sa.email}"]
}


# Génération de la clé d'accès pour le Service Account
resource "google_service_account_key" "cloud_run_sa_key" {
  service_account_id = google_service_account.cloud_run_sa.id
  key_algorithm      = "KEY_ALG_RSA_2048"
  private_key_type   = "TYPE_GOOGLE_CREDENTIALS_FILE"
}

# Déploiement de l'application sur Cloud Run
resource "google_cloud_run_service" "app_service" {
  name     = "cloud-run-app"
  location = var.REGION

  template {
    spec {
      containers {
        image = "gcr.io/${var.ID}/flask-tp-ci-cd"
        env {
          name  = "BUCKET"
          value = var.BUCKET
        
	}

      }
    service_account_name = google_service_account.cloud_run_sa.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
  
}


data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.app_service.location
  project     = google_cloud_run_service.app_service.project
  service     = google_cloud_run_service.app_service.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
