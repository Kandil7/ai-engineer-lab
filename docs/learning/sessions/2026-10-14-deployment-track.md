# Deployment learning track created (4 files, verified)

### Context

ai-engineer-lab, projects/06-devops/deployment/. Goal: create lecture, glossary, 15-question quiz, and a stdlib-only K8s manifest static analyzer exercise, matching the docker track's gold-standard format. Read the four docker track files fully first, plus deployment/README.md and the real deploy artifacts (Dockerfile, compose, render.yaml, railway.toml, deploy/README.md) to ground every claim.

### Explanation

Files created, with final line counts: lectures/01-deployment-strategies-lecture.md (610), lectures/01-deployment-strategies-glossary.md (577), quizzes/01-deployment-strategies-quiz.md (346), exercises/01-deployment-strategies.py (877). Zero existing files modified. Verification evidence: py_compile exit 0; demo exit 0 with bad sample 13 findings (5 critical, 6 warning, 2 info across all 8 rules) and good sample 0 findings; 15 mutation cases all pass (each rule proven to fire when its construct is removed, plus 4 no-false-positive guards: init containers, cluster-scoped Namespace, Job probe exemption, baseline good sample); the README's own example Deployment yields exactly 2 findings, both genuine (`:latest` tag, missing runAsNonRoot); CRLF=0 and em-dash=0 on all 4 files; all six workspace validators exit 0. Quiz integrity: 15 questions, 15 details blocks, difficulty mix Easy 6 / Medium 7 / Hard 2, Answer Key matches per-question answers, footer is `*Generated for ai-engineer-lab - Quiz 01 of 01*` (deliberately different from docker's footer, per task spec). Key discoveries for future track work: (1) infra/k8s/ exists only as an illustrative tree inside deployment/README.md, never cite it as a real path; (2) the real K8s-shaped teaching example in that README (auth-service, namespace fslab) is verified at README:53-78 and my lecture mirrors its shape; (3) compose line numbers verified: POSTGRES_PASSWORD :11, LANGFUSE interpolation :124, ANTHROPIC_API_KEY :127, devmate-api limits block :155-160 (2G/1G at :158/:160), named volumes :213-217; Dockerfile HEALTHCHECK :55-56; render.yaml healthCheckPath :29, RATE_LIMIT_REQUESTS 20 at :50-51, sync:false :64-67, generateValue :69; railway.toml healthcheckPath :12; deploy/README rollback :64, cold starts :69, free-plan caveats :74. (4) A dataclass-bearing module loaded via importlib must be registered in sys.modules before exec_module or `_is_type` raises AttributeError. (5) The other three tracks (docker, ci-cd, llmops) follow the identical 4-file pattern with quizzes all at 346 lines and exercises ranging 511-722 lines; all are uncommitted, only README+.gitkeep are tracked under projects/06-devops/.

### Alternatives

Considered building the exercise around PyYAML (ruamel/pyyaml) instead of a hand-rolled line parser: rejected because the task specified stdlib-only so it runs anywhere without env setup. Considered embedding a third (partially-good) sample: rejected as redundant since the mutation suite already proves every rule individually.

### Rationale (Why this?)

The exercise chose severities deliberately: critical for K8S001/K8S006/K8S008 (they silently break rollback, privilege isolation, or autoscaling), warning for the resource and probe gaps, info for namespace drift. K8S003 fires even when only limits are set because Kubernetes defaults requests to limits, but the message phrasing avoids claiming breakage. Probes are exempt for init containers and for Job/CronJob kinds, and namespace checks are exempt for cluster-scoped kinds such as Namespace itself; without those exemptions the analyzer would emit false positives on correct manifests. The lecture labels every README-sourced example as a teaching example so nobody runs kubectl against fictional paths.

### Exercises

Run the analyzer against a real manifest you own and triage each finding by severity, not alphabetically. Break the good sample deliberately (drop the namespace, delete requests, use :latest) and confirm exactly one rule fires each time. Write the section 16 manifest from memory, then diff it against the lecture. Convert one guessed alert threshold in your own stack into an SLO with a burn-rate expression. Time a rollout undo with kubectl rollout status and identify which portion is the readiness gate.

### Next Steps

Tracks docker, ci-cd, llmops, and deployment now all exist uncommitted; the user decides when to commit. Possible follow-ups: a CI job that runs each track's exercise in demo mode, or a fifth track (the README inventory lists more). See also docs/learning/paths/production-ai-systems-engineering.md which predates this session.

---
