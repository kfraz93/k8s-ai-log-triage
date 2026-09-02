# Kubernetes & Kind Local Development Commands

Quick reference for managing, inspecting, and troubleshooting the `k8s-ai-log-triage` local Kubernetes environment.

---

## 1. Docker & Image Management

* **Build application image:**
  ```powershell
  docker build -t k8s-ai-log-triage:v1.0 .
  ```
  *Compiles the multi-stage Dockerfile into a local tagged container image.*

---

## 2. Kind Cluster Operations

* **Create local cluster with port mappings:**
  ```powershell
  kind create cluster --config k8s/kind-config.yaml --name ai-log-triage
  ```
  *Spins up a local Kubernetes cluster inside Docker, mapping host port 8000 to NodePort 30080.*

* **Load local Docker image into kind:**
  ```powershell
  kind load docker-image k8s-ai-log-triage:v1.0 --name ai-log-triage
  ```
  *Transfers your locally built image directly into the kind node container so Kubernetes can use it without downloading from Docker Hub.*

* **Delete local cluster:**
  ```powershell
  kind delete cluster --name ai-log-triage
  ```
  *Tears down the entire local cluster and frees up Docker resources.*

---

## 3. Deployment & Kustomize

* **Apply all Kubernetes manifests and secrets via Kustomize:**
  ```powershell
  kubectl apply -k .
  ```
  *Parses root `kustomization.yaml`, injects `.env` variables into a Kubernetes Secret, and applies all resource definitions.*

* **Apply with parent directory override (if kustomization.yaml is inside k8s/):**
  ```powershell
  kubectl apply -k k8s/ --load-restrictor LoadRestrictionsNone
  ```
  *Bypasses Kustomize's folder boundary check to read the root `.env` file.*

* **Delete all applied resources:**
  ```powershell
  kubectl delete -k .
  ```
  *Removes all active Deployments, Services, and Secrets managed by Kustomize.*

---

## 4. Inspection & Troubleshooting

* **Check status of all key resources:**
  ```powershell
  kubectl get pods,svc,secrets
  ```
  *Lists active Pods, Services, and generated Secrets with their status and IPs.*

* **Stream live application container logs:**
  ```powershell
  kubectl logs -l app=ai-log-triage --tail=50 -f
  ```
  *Follows output logs for all pods matching the label `app=ai-log-triage`.*

* **Inspect pod configuration details and events:**
  ```powershell
  kubectl describe pod -l app=ai-log-triage
  ```
  *Shows detailed configuration, state transitions, container lifecycle status, and failure events.*

---

## 5. Local Endpoint Verification

* **Test application health endpoint from PowerShell:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/healthz"
  ```
  *Validates end-to-end host-to-pod networking through NodePort routing.*
