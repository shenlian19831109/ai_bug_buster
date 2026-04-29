## AI Assistant: Stubborn Bug Diagnosis and Breakthrough Algorithm (The 3-Round Rule)

When conventional "whack-a-mole" debugging fails, you MUST stop blind attempts and instead execute this systematic process.

### 1. Trigger Mechanism
- **Automatic Trigger**: The same error message or test failure persists or recurs after 2-3 consecutive repair attempts.
- **Manual Trigger**: User explicitly states keywords such as `timeout`, `still error`, `3 rounds`, `stubborn diagnosis`, or `feeling stuck`.

### 2. Core Execution Flow

#### Step 1: State Snapshot and Rollback Confirmation
Before any new attempts, establish a baseline:
1.  **Obtain Full Error**: Request the latest complete stack trace from the user.
2.  **Identify Rollback Point**: Find the last known working version (e.g., Git commit hash, previous successful conversation turn, or backup file).
3.  **Clean Up Environment**: If the current code is messy due to multiple attempts, suggest rolling back to a known good state for fresh analysis.

#### Step 2: Diagnostic Decision Tree (Categorize Error Causes)
Systematically check the following four dimensions in order. DO NOT skip dimensions.

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
Consider using a script like `bug_cracker.py` (provided in `src/bug_cracker.py`) to assist in analyzing logs and generating diagnostic reports.

### 4. Best Practices
-   **Avoid Ambiguity**: Do not say "Perhaps try...", instead say "Based on Dimension B's diagnosis, I recommend the following modification...".
-   **Mandatory Testing**: Every proposed fix MUST be accompanied by a verification step.
-   **Respect Rollback**: If two consecutive MVF attempts fail, strongly recommend rolling back to the snapshot point from Step 1.
