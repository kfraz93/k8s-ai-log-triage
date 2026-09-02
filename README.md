# AI-Powered Kubernetes Log Triage & Anomaly Service (`k8s-ai-log-triage`)

An enterprise-grade, cloud-native microservice built with **FastAPI**, **PostgreSQL (`pgvector`)**, **Ollama**, and **Kubernetes**.

The system provides an automated **AIOps Incident Engine** that ingests application and cluster error logs, executes vector similarity searches against historical incident resolutions in PostgreSQL, and leverages a local open-weight LLM (`qwen2.5`) to generate structured root-cause diagnoses, remediation steps, and executable `kubectl` diagnostic commands.

---

## Core Objectives & Workflow

* **Automated Log Ingestion & RAG Triage:** Ingests live error logs (manually via API or automatically via webhooks/log forwarders like Fluentbit or Alertmanager) and converts error messages into 768-dimensional embeddings using `nomic-embed-text`.
* **Context-Grounded Analysis (`pgvector`):** Performs cosine similarity searches (`<=>`) against a historical knowledge base of resolved incidents to supply real operational context, preventing LLM hallucinations.
* **Structured AI Diagnoses:** Leverages `qwen2.5:3b` via Ollama to produce strict JSON responses containing root cause analysis, confidence scores, human-readable remediation steps, and copy-pasteable `kubectl` commands.
* **Zero-Cloud-Cost Local Dev to Production IaC:** Fully runnable on local Kubernetes (`kind`) with zero cloud cost, alongside production-ready **Terraform** configurations for **Azure Kubernetes Service (AKS)** and GitHub Actions CI/CD pipelines.

---

## System Architecture

```mermaid
graph TD
    Client[External Client / Monitoring Webhook / Alertmanager] -->|HTTP POST /api/v1/triage| Ingress[NGINX Ingress Controller]
    Ingress --> Service[K8s ClusterIP Service]
    Service --> Pod[FastAPI + Async Python Pod]

    subgraph K8s [Kubernetes Cluster / Local 'kind' or AKS]
        Pod -->|1. Embed Error Query| Ollama[Ollama LLM Pod\nqwen2.5:3b / nomic-embed-text]
        Pod -->|2. Vector Search / pgvector| Postgres[(PostgreSQL StatefulSet\npgvector Enabled)]
        Postgres -->|3. Top-K Historical Incidents| Pod
        Pod -->|4. Context Injection & Prompt| Ollama
        Ollama -->|5. Structured JSON Diagnosis| Pod
    end

    Pod -->|6. Validated Triage Response| Client
