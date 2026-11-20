# Project success charter

**Status:** complete
**Last reviewed:** 2026-11-20

## Overall goal
- Outcome: Demonstrate a verifiably stronger direct-weight-only SmolLM2 checkpoint than both expanded-unedited and frozen V174 on independently controlled unseen coding repairs.
- Primary beneficiaries: The owner of the isolated local Smol800M direct-weight research experiment
- Why it matters: Distinguish real, reproducible generalization from exposed-task calibration and prompt-only improvement while preserving protected model runtimes.
- Time horizon: No fixed deadline; authorized bounded research milestones with independent acceptance before any release.

## Success metrics
| KPI | Why it matters | Baseline | Target / threshold | Evidence source | Review cadence |
| --- | --- | --- | --- | --- | --- |
| Unseen complete-code-repair pass-rate vs expanded baseline | Verify genuine code quality on independently sealed tasks | Unverified for paired unseen benchmark; historical exposed counts are not accepted | At least 10 absolute percentage points improvement and paired exact two-sided p<0.05 | Authenticated raw 192-token greedy responses, natural EOS, precommitted blind grading on at least 100 paired unseen tasks | Every separately authorized candidate evaluation |
| Unseen complete-code-repair pass-rate vs V174 | Show a new weight edit actually improves over frozen V174 | Frozen V174; no independent unseen score established | At least 5 absolute percentage points improvement and paired exact two-sided p<0.05 | Authenticated same-case V174 and candidate raw responses, exact checkpoint IDs and independent grader | Every separately authorized candidate evaluation |
| Retention and operational integrity | Avoid regressions and false claims | Current deployment/retention acceptance not established | No unacceptable predeclared retention loss; proven STOP/CANCEL/rollback and real resource/latency measurements | At least 20 precommitted retention cases and independently authenticated resource and worker receipts | Every candidate before promotion |

## Project acceptance criteria
- [x] G1 Independent authenticated protected worker provenance, key/response/replay custody, effective rights, source-bound QA.
- [x] G2 Owner-approved bounded 1750-second model lifecycle, cancellation, memory floors and complete rollback.
- [x] G3 Six exposed coding cases by two prompts, exact matched greedy decoding, complete raw/EOS and prompt-control accounting.
- [x] G4 One source-pinned direct-weight-only selective intervention with independent approval and no teachers/LoRA/fine-tuning.
- [x] G5 Independently controlled unseen paired quality/retention, significance, checkpoint hashes, hardware metrics and QA approval.

## Value rubric
- `critical`: required for project acceptance, safety, or a binding deadline.
- `high`: materially moves a priority KPI or unlocks critical/high-value work.
- `medium`: useful measurable contribution with limited leverage.
- `low`: weak, speculative, cosmetic, or currently unmeasured contribution.

When KPIs conflict, prefer: Safety and authentic owner authority > privacy and honest evidence > real coding accuracy > model speed.

## Constraints and non-goals
### Constraints
- The GitHub research-control repository is control-only (whether private or public); never upload local weights, datasets, raw logs, private local paths, security receipts, or secrets without separate review.
- Do not modify protected Luna services or bypass STOP/CANCEL; each full-model run requires genuine independent owner grant and verified rollback.
- No LoRA, conventional fine-tuning, teacher distillation or fake performance claims; preserve all original model checkpoints.
- Use separate clean Git checkout; never link or automatically push the frozen ACTIVE source tree to public GitHub.

### Non-goals
- Claiming 9B/GPT-level performance or native 1M context without evidence
- Production release or Luna integration before independent QA
- Training/teacher/LoRA work outside the direct-weight-only experiment

### Unacceptable tradeoffs
- Weakened authentication, cancellation or rollback to accelerate progress
- Publishing confidential local research sources or credentials
- Claiming model-quality gain from synthetic layer tests or unverified self-reported scores

## Assumptions and open questions
- None recorded at initialization; add evidence-backed changes with history.

## Operating policy

- `[policy:backend]` **Canonical goal backend**: github_issues (customized from a ZzzOps default)
- `[policy:git_review_release]` **Git, review, and release**: Follow repository rules; otherwise keep one branch and PR per source-changing goal, continue descendants from each exact verified predecessor checkpoint, collect human PR approval at true queue exhaustion, and integrate in dependency order. Policy review remains required before execution; required checks, human merge approval, and release authority are never bypassed. (adopted from the recorded ZzzOps default)
- `[policy:execution_continuation]` **Execution and work continuation**: Continue across actionable goals under reviewed dependency and resource policy, and incorporate newly captured goals at the next safe checkpoint. (adopted from the recorded ZzzOps default)
- `[policy:verification_testing]` **Verification and testing**: Require artifact-appropriate observable evidence in small chunks; documentation and test cases need no recursive tests, while product behavior and reusable test infrastructure require direct verification. (adopted from the recorded ZzzOps default)
- `[policy:code_quality]` **Code-quality and refactoring boundaries**: Preserve behavior unless a goal explicitly authorizes a behavior change. (adopted from the recorded ZzzOps default)
- `[policy:dependencies_tooling]` **Dependencies, tooling, and generated artifacts**: Use project-native tooling; do not hand-edit generated or dependency-owned files. (adopted from the recorded ZzzOps default)
- `[policy:security_privacy_compliance]` **Security, privacy, secrets, and compliance**: Repository policy may tighten but never weaken ZzzOps safety and authority boundaries. (customized from a ZzzOps default)
- `[policy:documentation_style]` **Documentation and style**: Follow evidenced repository documentation, style, and user-communication conventions. (adopted from the recorded ZzzOps default)
- `[policy:deployment_resources]` **Deployment, environment, and resources**: Do not deploy without authority; choose bounded parallelism from the deterministic tracked-file repository size. (adopted from the recorded ZzzOps default)
- `[policy:engineering_rigor]` **Engineering rigor**: structured (adopted from the recorded ZzzOps default)
- `[policy:workflow_adherence]` **ZzzOps workflow adherence**: tracked (adopted from the recorded ZzzOps default)
- `[policy:automated_design]` **Automated design authority**: enabled (adopted from the recorded ZzzOps default)
- `[policy:autonomy_approval_parallelism]` **Autonomy, approvals, and parallelism**: Interview adaptively during goal capture; execute unattended by persisting consequential questions as durable blockers; refill valuable bounded work; use up to three worktree workers below 100 MB and read-only workers otherwise. (adopted from the recorded ZzzOps default)

Detailed rationale and review history: [PROJECT_AUDIT.md](PROJECT_AUDIT.md). Canonical policy state: [POLICY.json](POLICY.json).
