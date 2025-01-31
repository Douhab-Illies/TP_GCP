#output "bucket_name" {
#  description = "Nom du BUCKET"
#  value       = google_storage_bucket.sto_illies.name
#}

output "url_app" {
  description = "ULR APP"
  value	      = google_cloud_run_service.app_service.status[0]
}
