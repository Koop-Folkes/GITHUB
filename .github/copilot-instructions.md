<!--
This file is generated to help AI coding agents become productive quickly in this repository.
If the repo already had a `copilot-instructions.md`, this file should be merged with preserving existing content.
-->
# Copilot instructions for this repository

Purpose
- Provide concise, project-specific guidance for AI coding agents working in this repo.

How to discover the project's shape (run these in `zsh` at repo root)
- Identify language and tooling:
  - `[[ -f package.json ]] && cat package.json | jq -r .name` — Node/npm workspace
  - `[[ -f pyproject.toml ]] && sed -n '1,60p' pyproject.toml` — Python/poetry/pyproject
  - `[[ -f Cargo.toml ]] && sed -n '1,60p' Cargo.toml` — Rust
  - `ls -1 | egrep '^(src|packages|services|apps)$'` — common monorepo/service layout
- Quick, general discovery commands:
  - `git status --porcelain --untracked-files=no` — check current branch/changes
  - `find . -maxdepth 2 -type f -name 'README.md' -print` — locate top-level READMEs
  - `rg --hidden --glob '!node_modules' 'TODO|FIXME|EXAMPLE' || true` — search for intent markers

Architecture / Patterns to look for
- Top-level `packages/` or `apps/` → monorepo. Look for `package.json` with `workspaces`.
- `services/*` or `api/*` → microservices. Expect each service to have its own Dockerfile, README, and tests.
- `src/` with `index.*`, `server.*`, or `app.*` → single-service app
- `infra/`, `deploy/`, or `terraform/` → infrastructure-as-code; be conservative modifying these files.

Developer workflows (what agents should run/check)
- Install/build (choose based on detected files):
  - Node: `npm ci && npm run build` or `pnpm install && pnpm -w -r build` for workspaces
  - Python: `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt` or `poetry install`
  - Rust: `cargo build --workspace`
- Tests:
  - Node: `npm test` or `pnpm -w -r test`
  - Python: `pytest -q`
  - Run the tests for the specific package/service that changed rather than running everything in a large monorepo.

Project-specific conventions (follow these when present)
- Minimal change rule: prefer small, single-responsibility edits and add tests for behavior you change.
- Code style: follow existing formatter (look for `.prettierrc`, `pyproject.toml` [tool.black], or `rustfmt.toml`) — do not reformat large files.
- Commit and PR messaging: keep changes scoped; include `#issue` or ticket if present in branch name.

Integration points and external dependencies
- Look for environment files (`.env.example`) and `README.md` sections describing external services (databases, APIs, SSO).
- When interacting with external APIs, preserve tokens and credentials — always use placeholders or `.env` changes only.

When to ask the user / create a human checkpoint
- If a change touches `infra/`, `deploy/`, CI workflows (`.github/workflows`), or public API signatures, stop and ask for approval.
- If repository has no clear build/test commands, list discovered files and ask which framework or package manager to target.

Examples (what to search for in this repository)
- If you see `package.json` with `workspaces`: run `pnpm -w -r build` instead of a single `npm run build`.
- If you see `services/*/Dockerfile`: prefer building locally with the service's `Dockerfile` target; do not push images.
- If a Python package has `pyproject.toml` with `[tool.black]`: use `black --check` rather than reformatting without consent.

Behavioral rules for the agent
- Make the minimal change necessary to implement the request.
- Avoid changing code outside the files directly required by the task.
- Add concise tests for any non-trivial logic change; run only the affected tests locally before proposing a patch.
- When uncertain, add a short comment `// TODO: confirm with maintainer` (or `# TODO`) and ask the user.

If this repository appears empty
- The repo currently contains no discoverable project files. Before making changes, report back with:
  - list of top-level files and directories (`ls -la`)
  - which language or framework you want me to target

Next steps for human reviewer
- Review this file for project-specific additions (CI commands, package managers, or non-standard workflows) and update accordingly.

If anything here is unclear or you want agent behavior adjusted, reply with specifics and I will iterate.
