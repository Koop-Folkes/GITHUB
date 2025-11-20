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
