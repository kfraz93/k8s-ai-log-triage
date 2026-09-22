terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 3.2.1"
    }
  }
}

provider "docker" {
  # Omitting the hardcoded Unix socket allows auto-detection
  # for Windows (npipe) and Linux/macOS (unix socket).
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "kind-ai-log-triage" # Matches your kind-config.yaml cluster name
}

# Managed local development namespace
resource "kubernetes_namespace_v1" "ai_triage" {
  metadata {
    name = "ai-log-triage"
    labels = {
      environment = "local-development"
      managed-by  = "terraform"
    }
  }
}
