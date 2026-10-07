---
id: system_improvement_p3
reported_by: opencode
created_at: 2026-10-07T08:46:04.574Z
---

System improvement P3 completed 2026-10-07. Facts: (1) task.implementation-planner KEPT: registry marks status deprecated + used_by [] + deprecated_in_favor_of role.project-planner; validator passes it by design; deletion would remove a tested path for nothing. (2) review-log outcome column ALREADY EXISTS (decision + score fields). (3) Executed: git rm -r --cached outputs/ (77 PNGs) + tracked .coverage; files confirmed on disk; repo-structure validator + docs gates green after. (4) .code-review-graph/ is ignored via global exclude (!! in porcelain --ignored), not repo gitignore - no action. (5) Tooling note: git check-ignore without --no-index exits 1 on tracked files here; use --no-index to test pattern matches. (6) The full improvement arc is closed: P0 truth restoration, P1 uv adoption + gates, P2 audit gating + review quick wins, structural splits + API tests, P3 hygiene. Open: A2 product work, first master push for ubuntu CI verification, commit decision.
