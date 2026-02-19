resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repository_name
  description   = "Docker repository for VigilantiAI"
  format        = "DOCKER"

  depends_on = [google_project_service.artifactregistry]
}
