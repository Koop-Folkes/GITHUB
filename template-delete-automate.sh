#!/usr/bin/env zsh
set -euo pipefail

# Repos to delete (from your attachment). Edit if needed.
REPOS=(
  "cappie333/Copilot_Agents"
  "cappie333/geometrydash"
  "cappie333/Koop-Folkes"
  "cappie333/OpenAI"
  "cappie333/openai-workspace"
  "cappie333/Prompt-Engineering"
  "cappie333/prompts"
)

# Defaults
DRY_RUN=1
BACKUP=1
FORCE=${FORCE:-0}  # set FORCE=1 in env to skip final interactive confirmation
BACKUP_DIR="${PWD}/template-backups-$(date +%F_%H%M%S)"

usage() {
  cat <<EOF
Usage: $0 [--run] [--dry-run] [--no-backup] [--backup-only] [--list]
  --run         Perform deletions (default is dry-run)
  --dry-run     Show what would be done (default)
  --no-backup   Skip creating mirror backups (not recommended)
  --backup-only Create backups then exit
  --list        Print the repo list and exit
EOF
  exit 1
}

# parse args
while (( "$#" )); do
  case $1 in
    --run) DRY_RUN=0; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-backup) BACKUP=0; shift ;;
    --backup-only) BACKUP=1; DRY_RUN=1; BACKUP_ONLY=1; shift ;;
    --list) echo "Repos:"; printf '%s\n' "${REPOS[@]}"; exit 0 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

# prerequisites
if ! command -v gh >/dev/null 2>&1; then
  echo "Error: 'gh' (GitHub CLI) not found. Install it first: https://cli.github.com/"
  exit 2
fi

echo "Checking gh authentication..."
if ! gh auth status >/dev/null 2>&1; then
  echo "Please authenticate gh now (interactive):"
  gh auth login
fi
echo "gh is authenticated."

echo ""
echo "Planned actions:"
echo "- Backups: ${BACKUP:-0}"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "- Mode: DRY RUN (no deletions). Use --run to actually delete."
else
  echo "- Mode: EXECUTE (will delete repos)."
fi
echo ""
echo "Repositories:"
for r in "${REPOS[@]}"; do
  echo "  - $r"
done
echo ""

# Backup
if [ "${BACKUP}" -eq 1 ]; then
  mkdir -p "$BACKUP_DIR"
  echo "Backing up repositories to: $BACKUP_DIR"
  for repo in "${REPOS[@]}"; do
    # convert to dir-safe name: replace / with __
    dir_name="${repo//\//__}"
    target="${BACKUP_DIR}/${dir_name}.git"
    echo "  * Mirroring ${repo} -> ${target}"
    if [ -d "$target" ]; then
      echo "    (mirror already exists, skipping clone)"
      continue
    fi
    # Prefer SSH; fallback to HTTPS if SSH fails
    if git ls-remote "git@github.com:${repo}.git" >/dev/null 2>&1; then
      git clone --mirror "git@github.com:${repo}.git" "$target" || { echo "    ! mirror clone failed for ${repo}"; }
    else
      git clone --mirror "https://github.com/${repo}.git" "$target" || { echo "    ! mirror clone failed for ${repo} (HTTPS)"; }
    fi
  done
  echo "Creating tar.gz of backups..."
  tar -czf "${BACKUP_DIR}.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"
  echo "Backups saved at: ${BACKUP_DIR}.tar.gz"
fi

# If user only wanted backups
if [ "${BACKUP_ONLY:-0}" = "1" ]; then
  echo "Backup-only requested — exiting after backup."
  exit 0
fi

# If dry run, stop here after showing plan
if [ "$DRY_RUN" -eq 1 ]; then
  echo "DRY RUN complete. No repositories deleted."
  exit 0
fi

# Confirm final action
if [ "$FORCE" != "1" ]; then
  echo ""
  echo "FINAL WARNING: You are about to PERMANENTLY DELETE the above repositories from GitHub."
  echo "This will remove all code, issues, PRs, releases, wiki, and settings."
  echo ""
  read -r -p "Type DELETE (uppercase) to proceed: " CONFIRM
  if [ "$CONFIRM" != "DELETE" ]; then
    echo "Confirmation not received. Aborting."
    exit 3
  fi
else
  echo "FORCE=1 set in environment; skipping interactive confirmation."
fi

# Perform deletions
for repo in "${REPOS[@]}"; do
  echo ""
  echo "Deleting ${repo}..."
  # attempt interactive delete with gh
  if gh repo view "${repo}" >/dev/null 2>&1; then
    # Use gh repo delete --confirm to avoid prompt; still requires proper permissions
    if gh repo delete "${repo}" --confirm >/dev/null 2>&1; then
      echo "  -> Deleted ${repo}."
    else
      echo "  ! Failed to delete ${repo} via gh. Trying API as fallback..."
      # fallback using GitHub API with GITHUB_TOKEN (must have delete_repo scope)
      if [ -n "${GITHUB_TOKEN:-}" ]; then
        http_code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
          -H "Authorization: token ${GITHUB_TOKEN}" \
          -H "Accept: application/vnd.github.v3+json" \
          "https://api.github.com/repos/${repo}")
        if [ "$http_code" = "204" ]; then
          echo "  -> Deleted ${repo} via API."
        else
          echo "  ! API deletion failed with HTTP code $http_code."
        fi
      else
        echo "  ! No fallback GITHUB_TOKEN set; manual deletion required for ${repo}."
      fi
    fi
  else
    echo "  ! Repo ${repo} not found or you lack permission. Skipping."
  fi
done

echo ""
echo "All requested deletions attempted."
echo "Verify on GitHub web UI or with 'gh repo view OWNER/REPO' for each repo."
