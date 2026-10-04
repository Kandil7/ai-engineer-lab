# Prompt Evaluation Guide

How to evaluate, test, and regress prompts in this workspace.

---

## Why Evaluate Prompts?

Prompts are engineering artifacts. A change to a prompt can:
- Break downstream workflows that depend on it
- Introduce scope creep (prompt does too much)
- Violate constraints (format rules, anti-hallucination)
- Drift from the intended behavior

Evaluation catches these issues before they propagate.

## Golden Case Format

Each golden case is a markdown file in `golden-cases/` with this structure:

```markdown
# Golden Case: <prompt-id> — <scenario-name>

## Prompt Under Test
<!-- Which prompt ID from prompt-registry.yaml -->
- **ID**: role.pair-programmer
- **Version**: 1.0.0

## Input Scenario
<!-- The user message or context that triggers the prompt -->
User asks to add API-key authentication to a FastAPI service.

## Expected Behavior
<!-- What the prompt SHOULD produce -->
1. Outputs step-by-step plan, not full code
2. Uses `secrets` module, not `random`, for key generation
3. Includes error handling for each step
4. References project file structure

## Pass Criteria
<!-- Specific, checkable conditions -->
- [ ] Response does NOT contain complete code blocks > 20 lines
- [ ] Response mentions `secrets` or secure random
- [ ] Response includes error handling
- [ ] Response references `projects/` directory
- [ ] Response length is between 200-2000 tokens

## Regression Tags
<!-- What this case protects against -->
- scope-creep
- security-misconfiguration
- format-violation
```

## Creating a Golden Case

1. **Identify the prompt**: Check `registries/prompt-registry.yaml` for the prompt ID
2. **Choose a scenario**: Pick a realistic user input that exercises the prompt
3. **Define expected behavior**: What should the prompt produce? Be specific.
4. **Write pass criteria**: 3-7 checkable conditions. Binary (pass/fail).
5. **Add regression tags**: Categorize what this case protects against

## Running Golden Cases

Golden cases are validated by the prompt regression workflow:

```powershell
# Validate all prompt golden cases
./infra/scripts/validate-prompts.ps1
```

The validator checks:
- All golden case files have required sections
- Referenced prompt IDs exist in the registry
- Pass criteria are non-empty

## Regression Test Setup

Regression files in `regressions/` track prompt changes over time:

```markdown
# Regression: <prompt-id> — <change-description>

## Change
What changed in the prompt (version bump, constraint added, etc.)

## Regression Checks
- [ ] Golden cases still pass
- [ ] No new scope creep detected
- [ ] Format rules still enforced
- [ ] Downstream workflows unaffected

## Date: 2026-06-26
## Changed By: <name>
```

## Running Prompt Audits

Use the `critic.prompt-auditor` prompt to audit a specific prompt:

1. Read the prompt file
2. Check against its constraints in `prompt-registry.yaml`
3. Verify format compliance
4. Flag scope creep or drift

The audit produces a report in `evaluations/prompts/regressions/`.

## Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| Golden case pass rate | % of golden cases passing | 100% |
| Constraint compliance | % of constraints satisfied | 100% |
| Scope drift | Number of unconstrained behaviors | 0 |
| Format violations | Missing required sections | 0 |

## Adding a New Evaluation Type

1. Create an ADR in `docs/decisions/` explaining the new evaluation
2. Add the evaluation type to this README
3. Create a validation script in `infra/scripts/` if needed
4. Register the script in `tests/` if it validates repo structure
