# Adding repository secrets (securely)

This repository uses GitHub Encrypted Secrets for CI and runtime values. Do NOT commit secret values to the repository.

Use the `gh` CLI to set secrets from your machine.

Examples (replace the values, or run interactively):

```bash
# Set OpenAI API key
gh secret set OPENAI_API_KEY --body "$OPENAI_API_KEY"

# Set a token used by automation (example)
gh secret set AUTOMATION_TOKEN --body "$AUTOMATION_TOKEN"

# Set multiple secrets interactively (safer)
read -s -p "Enter OPENAI_API_KEY: " OPENAI_API_KEY && echo
gh secret set OPENAI_API_KEY --body "$OPENAI_API_KEY"

read -s -p "Enter AUTOMATION_TOKEN: " AUTOMATION_TOKEN && echo
gh secret set AUTOMATION_TOKEN --body "$AUTOMATION_TOKEN"
```

Notes:
- `gh auth login` must be configured and authorized with a user who has `admin` access to the repository.
- Secrets set with `gh secret set` are stored encrypted and are available to GitHub Actions workflows when referenced as `${{ secrets.NAME }}`.
- Consider using organization-level secrets for shared CI values.
