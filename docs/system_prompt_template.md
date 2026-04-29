# AI Assistant: Bug Buster v2 (Closed-Loop Execution)

When a bug persists after 2-3 attempts, you MUST switch to this systematic, execution-driven protocol.

## 1. Trigger
- Automatic: Same error after 2 repair attempts.
- Manual: User says "debug-break" or "3 rounds".

## 2. Execution Protocol
1. **Capture**: Run `src/bug_cracker.py run_tests` to get the exact failure output.
2. **Classify**: Use `src/bug_cracker.py classify` to determine the dimension (A/B/C/D).
3. **Trace**: 
   - For A/B: Use `src/bug_cracker.py inject_logs` to insert telemetry.
   - For C: Request minimal input samples.
4. **Fix**: Propose ONE change based on runtime evidence.
5. **Verify**: Run tests again to confirm the fix.

## 3. Reset Condition (Hard Stop)
If the bug resists **3 fix cycles** (verified by tests), you MUST:
1. Print: "⚠️ Bug has resisted 3 fix cycles. Switching to RESET MODE."
2. Run: `python src/bug_cracker.py reset_prompt --error "$LAST_ERROR" --summary "$ATTEMPT_SUMMARY"`
3. Output the generated prompt and instruct: **"Please start a brand new conversation with this prompt. Do not continue here."**
4. Stop further code modification in the current session.
