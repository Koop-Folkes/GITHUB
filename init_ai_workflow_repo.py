#!/usr/bin/env python3
"""
init_ai_workflow_repo.py

Scaffolds a Template-centric AI workflow structure with:
- /global-memory/
- /prompts/
- /infra/secrets/
- /projects/
- /docs/
- README.md

Safe behaviour:
- Creates directories if missing
- Creates files ONLY if they do not already exist
- Never overwrites existing content
"""

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(".").resolve()

DIRS = [
    "global-memory",
    "prompts/system",
    "prompts/development",
    "prompts/design",
    "prompts/operations",
    "prompts/troubleshooting",
    "prompts/archived",
    "infra/secrets",
    "projects",
    "docs",
]

FILE_TEMPLATES = {
    "README.md": dedent(
        """\
        # Global AI Workflow & Knowledge Architecture

        This repository is the canonical source of truth for:
        - Global AI memory and rules
        - Prompt library
        - Workflow and process documentation
        - Secret registry metadata (no secret values)
        - Project-level documentation and structure

        ## Key Directories

        - `global-memory/` — global rules, standards, processes, tool usage
        - `prompts/` — global prompt library (with metadata in `index.json`)
        - `docs/` — global workflow and prompt-engineering guides
        - `infra/secrets/` — secret registry and policies (no values)
        - `projects/` — per-project docs, prompts, source, tests

        Template is canonical. SharePoint mirrors selected docs as read-only.
        """
    ),

    # --------------------
    # global-memory
    # --------------------
    "global-memory/memory.md": dedent(
        """\
        # 🌐 Global Memory

       This file defines global, long-lived organisational truths used by all AI tools.

       ## 1. Purpose

       - Provide a single, canonical place for global rules and knowledge.
       - Be referenced by ChatGPT, Codex, Atlas, CI, and any other AI tooling.
       - Avoid scattering “remember this” across chats and tools.

       ## 2. Global Rules (Examples – customise)

       - Template is the canonical knowledge base; SharePoint is a read-only mirror.
       - No secrets, API keys, tokens, or credentials are ever stored in:
          - Code
          - Prompts
          - Markdown docs
          - Chat logs
        - All process changes go through PRs on this repo.

       ## 3. Key References

       - `global-memory/standards.md`
       - `global-memory/processes.md`
       - `global-memory/tools.md`
        - `docs/workflow.md`
        - `docs/prompting.md`

        Extend this file over time with:
        - Permanent decisions
        - Global constraints
        - Company-wide conventions
        """
    ),

    "global-memory/glossary.md": dedent(
        """\
        # 📖 Global Glossary

       Shared terminology and naming conventions.

       ## Conventions

       - **Project** — A distinct deliverable, product, or initiative.
        - **Prompt** — A reusable instruction or template used with an AI model.
        - **Global Memory** — Org-wide rules/facts, applicable to all projects.
        - **Project Memory** — Facts and rules specific to a single project.

       ## Naming Patterns

       - ChatGPT project chats: `Project – <Name> – <Task>`
        - Repo folders:
          - `global-memory/`
          - `prompts/`
          - `projects/<project-name>/`

        Add domain-specific terms here as they stabilise.
        """
    ),

    "global-memory/standards.md": dedent(
        """\
        # 🧱 Standards (Coding, Design, Testing)

       This file defines global standards that all projects should follow.

       ## 1. Coding Standards (Examples – customise)

       - Use clear, descriptive names for variables, functions, and files.
       - Prefer composable, testable functions and modules.
       - Always include error handling and logging for external calls.

       ## 2. Design Standards

       - Follow platform-native design guidance (e.g. Apple HIG, Material Design).
        - Maintain consistent typography, spacing, and colour tokens across apps.
        - Ensure accessibility (contrast, font scaling, keyboard navigation).

       ## 3. Testing Standards

       - New features require unit tests where reasonable.
       - Critical flows require integration or end-to-end tests.
       - CI must run on every push to main and on PRs.

       ## 4. AI Usage Standards

       - When using AI for code:
          - Cross-check against official documentation if unsure.
          - Avoid deprecated or unstable APIs.
        - When using AI for documentation:
          - Review and correct for accuracy.
          - Ensure no confidential details are inadvertently exposed.

        Keep this file high-level and stable; project specifics go in project docs.
        """
    ),

    "global-memory/processes.md": dedent(
        """\
        # 🔁 Global Processes & Workflow

       This file captures the standard lifecycle used across projects.

       ## 1. Standard Phases

       1. Ideation & Planning
       2. Design
       3. Prototyping
       4. Development
       5. Testing & QA
       6. Deployment
       7. Documentation & Training

       ## 2. Global Process Rules

       - All phases must be documented in project-specific `docs/workflow.md`.
       - Significant decisions must be logged in project `docs/decisions.md`.
       - Changes to global process are done via PRs on this file.

       ## 3. Automation Principles

       - Automate repetitive tasks (scaffolding, testing, deployment) where possible.
       - Keep humans in the loop for:
          - Approving code changes
          - Approving production deployments
          - Approving major workflow changes
        """
    ),

    "global-memory/tools.md": dedent(
        """\
        # 🛠 Tool Usage Rules (AI & Dev Tools)

       Defines how AI tools and development tools should be used globally.

       ## 1. AI Assistants (ChatGPT, Codex, Atlas, etc.)

       - Always reference:
          - `global-memory/memory.md`
          - `global-memory/standards.md`
          - `global-memory/processes.md`
        - For project work, additionally reference:
          - `/projects/<project-name>/docs/`

       ## 2. Behavioural Rules for AI Tools

       - Never invent or store secrets.
       - Call out uncertainty and suggest verification steps.
       - When modifying code or docs:
          - Propose complete changes.
          - Avoid destructive actions (no blind deletes).

       ## 3. Knowledge Integration

       - Prefer official documentation (vendor docs, standards).
       - Summarise and cite key external sources in project docs.
        - Promote reusable knowledge from projects into `global-memory/` as needed.
        """
    ),

    # --------------------
    # prompts
    # --------------------
    "prompts/index.json": json.dumps([], indent=2) + "\n",

    # --------------------
    # infra/secrets
    # --------------------
    "infra/secrets/registry.yml": dedent(
        """\
        # 🔐 Secret Registry (Metadata Only)

        # This file tracks secret identifiers, ownership, and storage locations.
        # It MUST NOT contain actual secret values.

        secrets:
          - id: example_openai_api_key
            description: "Example OpenAI API key for CI or backend."
            owner: "platform-team"
            location:
              github_secret: "OPENAI_API_KEY"
              key_vault: "kv-prod-openai/openai-api-key"
            rotation: "90d"
            last_rotated: "YYYY-MM-DD"

        # Add real entries via PRs. Do not store secrets here.
        """
    ),

    "infra/secrets/policies.md": dedent(
        """\
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
        """
    ),

    # --------------------
    # docs
    # --------------------
    "docs/workflow.md": dedent(
        """\
        # 🌐 Global AI Workflow Model

       This document defines the standard lifecycle to be reused across projects.

       ## 1. Phases

       1. Ideation & Planning
       2. Design
       3. Prototyping
       4. Development
       5. Testing & QA
       6. Deployment
       7. Documentation & Training

       Projects may extend or specialise this in `/projects/<name>/docs/workflow.md`.

       ## 2. Phase Overview (High-Level)

       - **Ideation & Planning** — clarify goals, constraints, and stakeholders.
       - **Design** — UX, technical design, architecture, and interfaces.
       - **Prototyping** — rapid validation of approach and core flows.
       - **Development** — feature implementation, refactor, and hardening.
       - **Testing & QA** — automated + manual, including non-functional.
       - **Deployment** — packaging, rollout, monitoring setup.
       - **Documentation & Training** — user docs, runbooks, onboarding material.

       ## 3. Governance

       - This file is global. Projects inherit from it and may specialise locally.
       - Any change here should be considered a cross-project process change.
        """
    ),

    "docs/prompting.md": dedent(
        """\
        # 🧩 Prompt Creation & Revision Guide

       This guide defines how prompts are designed, tested, and maintained.

       ## 1. Prompt Types

       - System / role prompts
        - Task / instruction prompts
        - Review / critique prompts
        - Refactor / improve prompts
        - Automation / ops prompts

       ## 2. Standard Prompt Template

       Use this structure for new prompts:

        ```text
        # Goal
        <What must be achieved>

        # Context
        <Relevant files, policies, workflows, memory references>

        # Inputs
        <Source material, logs, data>

        # Constraints
        <Rules, standards, frameworks, forbidden actions>

        # Output Format
        <Exact JSON, Markdown, steps, code>

        # Verification
        <What success looks like>

        # References
        /global-memory/memory.md
        /global-memory/standards.md
        /docs/workflow.md
        ```

        ## 3. Prompt Lifecycle

        1. Draft a minimal version.
        2. Test on simple representative inputs.
        3. Add constraints and clarify outputs.
        4. Add examples (few-shot) for complex tasks.
        5. Test edge cases and adversarial inputs.
        6. Document expected behaviour and limitations.
        7. Add to `/prompts/` and `prompts/index.json` with proper metadata.
        8. Archive superseded versions to `/prompts/archived/`.

        ## 4. Quality Rules

        - No secrets in prompts.
        - Must specify output format.
        - Must reference relevant global/project memory where useful.
        - Changes must be tracked via version and metadata.
        """
    ),

    # --------------------
    # projects (placeholder)
    # --------------------
    "projects/.gitkeep": "",
}


def ensure_directories():
    created = []
    for d in DIRS:
        path = ROOT / d
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(path.relative_to(ROOT)))
    return created


def write_file_if_missing(rel_path: str, content: str):
    path = ROOT / rel_path
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    # create new file, no overwrite
    with path.open("x", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    print(f"Initialising AI workflow structure under: {ROOT}")

    created_dirs = ensure_directories()
    if created_dirs:
        print("\n[+] Created directories:")
        for d in created_dirs:
            print(f"    - {d}")
    else:
        print("\n[=] All target directories already exist.")

    created_files = []
    skipped_files = []

    for rel_path, content in FILE_TEMPLATES.items():
        try:
            created = write_file_if_missing(rel_path, content)
        except FileExistsError:
            created = False

        if created:
            created_files.append(rel_path)
        else:
            skipped_files.append(rel_path)

    if created_files:
        print("\n[+] Created files (no overwrites):")
        for f in created_files:
            print(f"    - {f}")

    if skipped_files:
        print("\n[=] Skipped existing files (left untouched):")
        for f in skipped_files:
            print(f"    - {f}")

    print("\nDone. Review and commit the new structure to Git.")
    print("Reminder: add real secrets only to your secret managers, not to this repo.")


if __name__ == "__main__":
    main()
