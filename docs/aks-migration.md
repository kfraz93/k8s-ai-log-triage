cd terraform
(k8s-ai-log-triage) PS C:\Users\Lenovo\PycharmProjects\k8s-ai-log-triage\terraform> terraform init
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of kreuzwerker/docker from the dependency lock file
- Reusing previous version of hashicorp/kubernetes from the dependency lock file
- Using previously-installed kreuzwerker/docker v4.6.0
- Using previously-installed hashicorp/kubernetes v3.2.1


Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
(k8s-ai-log-triage) PS C:\Users\Lenovo\PycharmProjects\k8s-ai-log-triage\terraform> terraform plan
kubernetes_namespace_v1.ai_triage: Refreshing state... [id=ai-log-triage]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
(k8s-ai-log-triage) PS C:\Users\Lenovo\PycharmProjects\k8s-ai-log-triage\terraform> terraform apply
kubernetes_namespace_v1.ai_triage: Refreshing state... [id=ai-log-triage]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
