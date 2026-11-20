# ZzzOps project policy audit

Status: complete. Reviewer: Tich62. Revision: 2.

## Evidence and decisions

- [x] `[policy:backend]` **Canonical goal backend** (applicable)
  - Decision: github_issues
  - Rationale: ZzzOps GitHub Issues remains the sole backend, with verified exact repository identity and authenticated access; project-specific details customize the shipped default without weakening backend safety.
  - Sources: E-003: Official ZzzOps init inspect in isolated local public control checkout — Git origin verified; policy absent; GitHub CLI installed but not authenticated; GitHub repository not usable by local CLI.; E-005: 2026-11-20 authenticated GitHub CLI gh repo view and GitHub connected get_repo — Tich62/mol800M-DirectWeightResearch is currently private; connected app and local authenticated GitHub CLI both verify repository access. Local public-control checkout has a distinct origin and no contents or commits.
  - Confidence/default: medium; ZzzOps GitHub-only authority → changed
  - Provenance: customized from a ZzzOps default
  - Settings: `{"authority": "github_issues", "capability_evidence": "Local gh auth status exit 0, official init inspect github_auth.ok=true, github_repository.usable=true, git_origin.ok=true, connected GitHub get_repo confirms private repository identity and issue-management rights.", "fallback": "forbidden", "repository_identity": "Tich62/mol800M-DirectWeightResearch", "tradeoffs": {"github_issues": "shared native issue queue requiring GitHub access"}}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:git_review_release]` **Git, review, and release** (applicable)
  - Decision: Follow repository rules; otherwise keep one branch and PR per source-changing goal, continue descendants from each exact verified predecessor checkpoint, collect human PR approval at true queue exhaustion, and integrate in dependency order. Policy review remains required before execution; required checks, human merge approval, and release authority are never bypassed.
  - Rationale: maximizes safe unattended progress while preserving independently reviewable PR gates and an explicit stricter per-goal alternative
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps exhaustion-time review fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"branch_base": "nearest_authorized_trunk", "child_target": "nearest_parent_branch", "commit_style": "conventional", "commit_unit": "verified_subgoal", "conversational_approval": "never_for_goal_progress", "dependency_base": "dependency_branch", "execution_branch": "per_goal", "merge_after_approval": "when_authorized", "multiple_dependency_base": "reviewed_base_containing_all", "parent_pseudo_trunk": true, "pr_approval": "required_when_repository_requires_pr", "pull_request_unit": "per_goal", "read_only_dependency_investigation": "allowed_before_completion", "review_gate": "human_at_exhaustion", "review_pending_dependency": "stack_from_reviewed_checkpoint", "review_state_reads_per_checkpoint": 1, "shared_pull_request": "explicit_reviewed_override"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:execution_continuation]` **Execution and work continuation** (applicable)
  - Decision: Continue across actionable goals under reviewed dependency and resource policy, and incorporate newly captured goals at the next safe checkpoint.
  - Rationale: reduces babysitting without forcing sequential work when bounded parallelism is safe
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps first-release fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"after_additive_capture": "resume_once_and_reprioritize", "continue_while_actionable": true, "cross_task": "require_explicit_harness_signal", "execute_intent": "same_task_until_superseded", "exhausted_handoff_retains_intent": true, "human_unblock_watch": {"enabled": false, "max_blockers": 1, "max_seconds": 180, "notify_once": true, "poll_seconds": 30, "trigger": "disabled_for_unattended_execution"}, "max_easy_wins": 2, "new_goal_checkpoint": "next_safe_checkpoint", "stop_reasons_clear_intent": ["user_stop", "pause", "replacement_request", "capture_only", "required_authority", "blocking_boundary"], "triage_new_first": true}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:verification_testing]` **Verification and testing** (applicable)
  - Decision: Require artifact-appropriate observable evidence in small chunks; documentation and test cases need no recursive tests, while product behavior and reusable test infrastructure require direct verification.
  - Rationale: prevents unobservable product changes and false confidence without manufacturing documentation or test meta-tests
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: high; ZzzOps observable-work fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"artifact_verification": {"documentation": "inspect_artifact_no_feature_test", "product_runtime": "risk_proportionate_behavioral_probe", "test_cases": "run_changed_tests_no_recursive_meta_test", "test_harness": "focused_behavioral_regression"}, "ci_deduplication": {"failure": "inspect_logs_and_reprobe", "local_probe": "smallest_unique_falsifiable_signal", "required_ci": "inspect_exact_pr_head", "skip_broad_local_when": "same_command_required_ci", "unavailable": "durable_blocker"}, "mode": "chunk_probe", "test_bug": "capture_and_ask", "widen": "as_relevant"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:code_quality]` **Code-quality and refactoring boundaries** (applicable)
  - Decision: Preserve behavior unless a goal explicitly authorizes a behavior change.
  - Rationale: separates cleanup from product decisions
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps conservative fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"completion_self_review": "required_before_review_or_done", "dead_code": "remove_only_if_evidenced_and_in_scope", "dynamic_generated_vendor": "retain_without_proof", "non_behavioral_only_without_feature_goal": true, "record_clean_review": true, "reverify_after_changes": true, "review_scope": "goal_diff_tests_and_relevant_surroundings"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:dependencies_tooling]` **Dependencies, tooling, and generated artifacts** (applicable)
  - Decision: Use project-native tooling; do not hand-edit generated or dependency-owned files.
  - Rationale: replace with repository-specific commands and ownership evidence
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps conservative fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"dependency_changes": "explicit_scope", "generated_files": "source_or_generator_only", "tooling": "project_native"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:security_privacy_compliance]` **Security, privacy, secrets, and compliance** (applicable)
  - Decision: Repository policy may tighten but never weaken ZzzOps safety and authority boundaries.
  - Rationale: Customize the shipped least-privilege privacy default with explicit local protected runtime noninterference and private checkpoint/public-repository control separation.
  - Sources: E-001: GitHub Issue #1 (repository currently private) — Owner's direct-weight SmolLM2 outcome, five goal gates and blockers are tracked in an open issue.; E-003: Official ZzzOps init inspect in isolated local public control checkout — Git origin verified; policy absent; GitHub CLI installed but not authenticated; GitHub repository not usable by local CLI.; E-004: Read-only frozen research checkpoint and archived tests — V174 research overlay is immutable, and no independent unseen model-improvement evidence has been accepted.; E-005: 2026-11-20 authenticated GitHub CLI gh repo view and GitHub connected get_repo — Tich62/mol800M-DirectWeightResearch is currently private; connected app and local authenticated GitHub CLI both verify repository access. Local public-control checkout has a distinct origin and no contents or commits.
  - Confidence/default: medium; immutable ZzzOps boundary → changed
  - Provenance: customized from a ZzzOps default
  - Settings: `{"production_mutation": "explicit_authority", "project_constraints": ["No public upload of local weight files, private datasets, source checkout or protected security receipts without review", "No model inference, weight edits, production Luna changes, or deployment without genuine action-specific owner authorization", "Stop/cancel, independent security custody and complete rollback are mandatory"], "secrets": "never_expose"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:documentation_style]` **Documentation and style** (applicable)
  - Decision: Follow evidenced repository documentation, style, and user-communication conventions.
  - Rationale: keep communication project-appropriate while providing a concise ZzzOps fallback
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps fallback overridden by repository or user evidence → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"communication": {"style": "outcome_first", "technical_detail": "decision_risk_failure_or_request", "user_action": "one_clear_action_with_reason_and_next_step"}, "documentation": "repository_conventions", "style": "repository_conventions"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:deployment_resources]` **Deployment, environment, and resources** (applicable)
  - Decision: Do not deploy without authority; choose bounded parallelism from the deterministic tracked-file repository size.
  - Rationale: limits external impact and avoids multiplying large writable checkouts
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps conservative fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"delegate_wait_after_seconds": 60, "deployment": "explicit_authority", "resource_mode": "size_aware"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:engineering_rigor]` **Engineering rigor** (applicable)
  - Decision: structured
  - Rationale: Balance production-oriented specification and verification with escalation-ready harness investment; higher-risk work can automatically require agentic evidence.
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps production-oriented fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"escalation": {"allow_automatic_deescalation": false, "allow_automatic_escalation": true, "enabled": true}, "minimums": {"authentication": "agentic", "authorization": "agentic", "destructive_data_migrations": "agentic", "payments": "agentic", "secrets": "agentic", "security_sensitive": "agentic", "throwaway_prototypes": "vibe"}, "overrides": {"lowering": "explicit_user_authority", "may_undercut_risk_minimum": false, "per_goal": true, "raising": "allowed"}, "requirements_interview": {"level_mapping": {"agentic": "thorough", "structured": "standard", "vibe": "light"}, "source": "effective_engineering_rigor"}}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:workflow_adherence]` **ZzzOps workflow adherence** (applicable)
  - Decision: tracked
  - Rationale: Require durable goal context for substantial agent work while allowing projects to review stricter or lighter routing.
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps tracked-work fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"agents_projection": "review_workflow_reconciliation", "exemptions": ["read_only_investigation", "zzzops_administration"], "levels": {"managed": "zzzops_workflow_required_for_repository_changes", "optional": "direct_agent_work_allowed", "tracked": "durable_goal_required_for_substantial_agent_work"}, "scoped_exception": "explicit_scoped_user_authority"}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:automated_design]` **Automated design authority** (applicable)
  - Decision: enabled
  - Rationale: Allow unattended execution to resolve low-commitment in-scope design choices when reviewed project evidence is decisive, escalate high-commitment choices through early evidence, and retain hard authority gates.
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps bounded-commitment automated-design fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"commitment": {"high": "compare_evidence_cost_signal_or_explicit_current_design_review", "low": "replace_verify_and_clean_within_one_goal_before_fanout", "structural_cost_signals": ["affected_goal_units", "started_descendant_branches", "started_descendant_prs", "durable_data", "public_or_integration_contracts", "external_state", "compatibility_paths", "verification_breadth", "clean_removal_path"]}, "decision_record": ["alternatives", "rationale", "assumptions", "falsifiable_validation_signal"], "hard_stops": ["product_scope", "incompatible_public_contract", "destructive_migration", "external_spending", "deployment", "external_write", "human_review", "safety_authority", "higher_authority"], "insufficient_evidence": "durable_design_blocker", "privacy_security": "unambiguously_risk_reducing_without_material_behavior_change", "scope": "bounded_commitment_in_scope_implementation", "selection_basis": ["project_objectives", "kpi_evidence", "constraints", "precedence"]}`
  - Exceptions: none
  - Unresolved: none
- [x] `[policy:autonomy_approval_parallelism]` **Autonomy, approvals, and parallelism** (applicable)
  - Decision: Interview adaptively during goal capture; execute unattended by persisting consequential questions as durable blockers; refill valuable bounded work; use up to three worktree workers below 100 MB and read-only workers otherwise.
  - Rationale: balances precise capture, unattended execution, authority, bounded valuable refill, and predictable repository resource cost
  - Sources: E-002: ZzzOps v2.1.0 official default policy — Project-specific policy sections and public repository security boundaries require explicit review and approved digest.
  - Confidence/default: medium; ZzzOps conservative fallback → accepted
  - Provenance: adopted from the recorded ZzzOps default
  - Settings: `{"blocker_interview": "capture_only", "blocker_order": ["safety_access_human", "cross_goal_decisions", "specification", "technical_unknown"], "capture_defaults": {"confidence": "low", "difficulty": "unknown", "priority": "P2"}, "claim_ttl_hours": 4, "dependency_implementation_gate": "stack_from_reviewed_checkpoint", "execution_reports": {"enabled": true}, "max_workers": 3, "parallelization": {"at_or_above_threshold_mode": "read_only", "below_threshold_mode": "worktrees", "measurement": "existing_git_tracked_worktree_bytes", "threshold_bytes": 104857600}, "planning": {"decompose_at": "L", "max_depth": 3}, "project_parallel_ceiling": "size_aware", "read_only_dependency_investigation": true, "refill": {"allowed_categories": ["documentation", "tests", "code_quality_non_behavioral"], "enabled": true, "max_per_run": 3}, "requirements_interview": {"capture_depth": "standard", "execution_questions": "durable_blockers_only", "mode": "adaptive", "stakeholder_model": "requesting_user_only"}, "resource_reservations": {"exclusive_prefixes": ["generated", "external"], "exclusive_resources": [], "mode": "conflict_tolerant"}, "worktree_lifecycle": {"abandoned_or_dirty": "forbidden", "after_task": "remove_or_retain_clean_for_reuse", "reuse_requires": ["clean_state", "reviewed_base", "new_goal_resources", "safe_branch_reassignment"]}}`
  - Exceptions: none
  - Unresolved: none

## Review record

| Date | Actor/run | Change | Reason/evidence |
| --- | --- | --- | --- |
| 2026-11-20 | ZzzOps initialization | Created pending revision 1 | Confirmed agent-generated draft; explicit policy review still required. |
| 2026-11-20 | Tich62 | Reviewed policy revision 2 | Approved: backend, git_review_release, execution_continuation, verification_testing, code_quality, dependencies_tooling, security_privacy_compliance, documentation_style, deployment_resources, engineering_rigor, workflow_adherence, automated_design, autonomy_approval_parallelism; source digest sha256:ad8e7fc1a37615a8e32158ec5e7fbf71dfd81d78e4fb9be37ea6c52f6260de61. |

The machine-readable authority is [POLICY.json](POLICY.json); this file is its human audit view.
