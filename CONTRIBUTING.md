# Contributing Guidelines

Thank you for considering contributing to the Business Ideas project! We welcome contributions from everyone.

## Coding standards

- Follow language-specific best practices (e.g., PEP8 for Python, ESLint/Prettier for JavaScript/TypeScript).
- Write clear and concise code with comments where necessary.
- Include unit tests for new functionality and ensure existing tests continue to pass.

## Branch naming conventions

Create branches off of `main` using the following prefixes:

- `feature/<short-description>` for new features and enhancements.
- `bugfix/<short-description>` for bug fixes.
- `task/<short-description>` for small tasks and chores.
- `research/<short-description>` for exploratory work.

Use hyphens to separate words (e.g., `feature/user-authentication`).

## Review and merge process (solo owner with collaborating agents)

The owner may preauthorize a bounded engineering/process workstream and have
independent agents implement and review it. A GitHub teammate, label, meeting,
or separate owner click is **not** required for every routine change. This is
not permission for an agent to approve its own work or invent an owner decision.

1. Create a branch from current `main` and open a PR. Include the objective,
   changed behavior, tests/evidence, remaining risks, and the applicable owner
   authorization or task. Link an issue when one already exists; new labels,
   issue tickets, and reviewer requests are optional, not release gates.
2. **Preauthorized low-risk work** includes internal documentation and process
   templates, tests, CI checks, and bounded bug fixes that do not change live
   business activity, security/privacy posture, or public product content. An
   independent agent/code reviewer should inspect nontrivial code and defects
   found in review must be corrected and retested. Record that review in the
   PR; do not misrepresent an AI review as approval by a GitHub team member.
3. For these low-risk PRs, require all applicable GitHub CI checks to succeed.
   When a changed path has no CI workflow, record an appropriate local test,
   lint, or link check. An authorized agent or maintainer may then merge
   without another owner approval, unless actual GitHub branch protection or
   a repository-specific safety rule requires more.
4. **Stop for owner direction** before customer outreach, purchases, filings,
   spending, real-world experiments, business/regulatory/financial decisions,
   confidential data, security/privacy or permissions changes, public-facing
   content launches, or other consequential external effects. Review evidence
   before treating an experiment as proof of demand. No agent may self-grant
   authority by editing a traveler or declaring a result approved.
5. If risk is uncertain, an existing PR has a stronger review promise, or a
   required check fails, leave the PR open with a clear blocker. Never bypass
   protected-branch rules. Preserve open PRs and unrelated branches. Squash
   merges are preferred; do not commit directly to `main`.

This risk-based policy replaces the previous blanket requirement for another
human team-member review of every PR. The owner expressly authorized removal
of ceremonial-only gates while retaining substantive controls on November 26,
2026. It does **not** retroactively approve separate business-content PRs.

## Code of conduct

Please be respectful and considerate in all interactions. We strive to create an inclusive and supportive environment for all contributors.
