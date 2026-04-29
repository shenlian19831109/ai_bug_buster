# AI-Assisted Stubborn Bug Diagnoser (The 3-Round Rule)

## Overview

This project provides a systematic methodology and tools for AI assistants to diagnose and resolve persistent software bugs, especially when conventional debugging approaches fail after multiple attempts. Inspired by the "3-Round Rule," this framework guides AI in moving beyond "whack-a-mole" fixes to a structured analysis, rollback, and minimal verifiable fix (MVF) approach.

## Motivation

In AI-assisted software development, it's common for AI models to attempt quick fixes based on immediate error messages. While often effective, this can lead to a "whack-a-mole" scenario where fixing one issue introduces another, or the same bug resurfaces repeatedly. The "3-Round Rule" aims to break this cycle by enforcing a disciplined diagnostic process when a bug proves stubborn.

## Core Methodology: The 3-Round Rule

When a bug persists after 2-3 consecutive repair attempts, or when the developer feels "stuck in a loop," the AI assistant MUST switch to this systematic diagnostic mode.

### 1. Trigger Mechanism

-   **Automatic Trigger**: The same error message or test failure persists or recurs after 2-3 consecutive repair attempts.
-   **Manual Trigger**: The user explicitly states keywords such as `timeout`, `still error`, `3 rounds`, `stubborn diagnosis`, or `feeling stuck`.

### 2. Core Execution Flow

#### Step 1: State Snapshot and Rollback Confirmation

Before any new attempts, establish a clear baseline:

1.  **Obtain Full Error**: Request the latest complete stack trace from the user.
2.  **Identify Rollback Point**: Find the last known working version (e.g., Git commit hash, previous successful conversation turn, or backup file).
3.  **Clean Up Environment**: If the current code is messy due to multiple attempts, suggest rolling back to a known good state for fresh analysis.

#### Step 2: Diagnostic Decision Tree (Categorize Error Causes)

Systematically check the following four dimensions in order. **DO NOT skip dimensions.**

| Dimension | Diagnostic Criteria | Typical Manifestations | Action Direction |
| :-------- | :------------------ | :--------------------- | :--------------- |
| **A. Local Logic Error** | Error points to specific, isolated code logic | Null pointer, index out of range, type mismatch, division by zero | Rewrite unit tests for the specific function/module, isolate and verify |
| **B. Context/State Pollution** | Error location shifts, fixing A breaks B | Deadlock, race condition, global variable conflicts, stale cache | Rollback, then focus on changing variable scope/data flow, rather than fixing the immediate error point |
| **C. Upstream Data/External Dependency** | Error only appears with specific inputs or environments | API response format changes, file encoding issues, time/timezone discrepancies | Request minimal input samples from the user, mock external calls for testing |
| **D. AI Model Blind Spot** | Involves complex concurrency, reflection, low-level system calls | Asynchronous callback order, generic type erasure, memory leaks | Cease direct code modification, generate detailed diagnostic logs, request human review |

#### Step 3: Minimal Verifiable Fix (MVF)

Output MUST contain ONLY:

1.  **A Single Core Change**: Strictly prohibit making multiple unrelated changes at once.
2.  **Verification Script/Command**: Provide specific test commands (e.g., `pytest`, `curl`) and expected output.
3.  **Rollback Plan**: Clearly state how to revert the change if it fails (e.g., `git revert <commit>` or comment out the change).

#### Step 4: Internal Self-Checklist (AI Internal Execution, NOT Output to User)

Before responding to the user, the AI MUST ask itself:

-   Does this solution require new information I haven't obtained yet? (If yes, ask for it first.)
-   If the user executes my solution and it still fails, what is the most likely secondary reason? (Inform the user of this expectation.)
-   Is there a simpler alternative (e.g., disabling a feature, downgrading a dependency, using a different algorithm)? (If yes, prioritize recommending it.)

### 3. Auxiliary Tools

-   `src/bug_cracker.py`: A Python script to assist in analyzing error logs and suggesting diagnostic dimensions based on keywords.

### 4. Best Practices for AI Assistants

-   **Avoid Ambiguity**: Do not say "Perhaps try...", instead say "Based on Dimension B's diagnosis, I recommend the following modification...".
-   **Mandatory Testing**: Every proposed fix MUST be accompanied by a verification step.
-   **Respect Rollback**: If two consecutive MVF attempts fail, strongly recommend rolling back to the snapshot point from Step 1.

## Integration with AI Assistants

This methodology can be integrated into various AI assistant platforms:

-   **System Prompt**: Embed the core execution flow into the AI's system prompt for general guidance.
-   **Custom Tool/Skill**: Implement as a custom tool or skill (e.g., Manus Skill, Cursor Skill) that can be explicitly invoked or automatically triggered.
-   **IDE Extensions**: Develop as an extension for IDEs (e.g., VS Code Copilot, Cursor) to provide context-aware suggestions.

## Installation and Usage

### For AI System Prompt Integration

Refer to `docs/system_prompt_template.md` for a ready-to-use system prompt template.

### For IDEs (e.g., Cursor, VS Code with Copilot)

Refer to `rules/ide_rules.md` for configuration snippets that can be added to `.cursorrules` or similar AI configuration files.

### For `bug_cracker.py`

```bash
python src/bug_cracker.py <path_to_error_log_file>
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests to improve this methodology and its accompanying tools.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
