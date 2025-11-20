 # 🔐 Secret Management Policies

## 1. Storage Locations

- CI/CD secrets:
   - GitHub Encrypted Secrets
 - Runtime application secrets:
   - Azure Key Vault / AWS Secrets Manager
 - Local developer secrets:
   - 1Password (or equivalent) with CLI integration
 - Org-wide non-secret config:
   - SharePoint Secure Library

## 2. Prohibited

- No secrets in:
   - Git repos (code or docs)
   - Prompt files
   - Chat logs
   - Issue trackers

## 3. Rotation

- High-sensitivity secrets: at least every 90 days.
 - Others: at least every 180 days.
 - Rotation events should update `infra/secrets/registry.yml` metadata.

## 4. Detection

- Recommended:
   - Pre-commit hooks with tools like Gitleaks/Trufflehog.
   - Regular scans of repositories for accidental secret commits.
