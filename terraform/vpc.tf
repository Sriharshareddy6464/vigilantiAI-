# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "vigilantiai-vpc"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.compute]
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "vigilantiai-subnet"
  region        = var.region
  network       = google_compute_network.vpc.id
  ip_cidr_range = "10.0.0.0/16"

  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# Cloud Router (for NAT)
resource "google_compute_router" "router" {
  name    = "vigilantiai-router"
  region  = var.region
  network = google_compute_network.vpc.id
}

# Cloud NAT (to allow private nodes to access internet)
resource "google_compute_router_nat" "nat" {
  name                               = "vigilantiai-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
