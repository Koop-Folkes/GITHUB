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
