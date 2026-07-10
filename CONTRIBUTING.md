<div align="center"> <!-- markdownlint-disable MD041 MD033 -->
  <img src="/assets/KEYBOARD_HAPPY_FLOYD.png" alt="Logo" width="150"/>
</div>

# Contributing to CPG Flow

We appreciate your interest in contributing to CPG Flow! This project, sponsored by the Centre for Population Genomics, has a global community of contributors who have added significant value over time. This guide outlines how we manage external contributions to maximize their impact and reduce delays in getting your pull requests (PRs) reviewed and accepted.

## Share your idea with us first

Before diving into writing a substantial amount of code, we recommend reaching out by submitting an [issue](https://github.com/populationgenomics/cpg-flow/issues/new) to gather feedback. We may offer advice on the best way to approach the problem, and in some cases, there might be unforeseen challenges that could affect your solution. Catching these early can save time and effort, and help prevent your PR from being rejected due to overlooked constraints.

## Consider maintenance

The CPG software team continuously maintains and improves the application to meet the needs of both internal and external users. There may be instances where we recognize a feature or contribution as valuable, but we might not have the capacity to maintain it long-term. This could be due to project priorities or time limitations on the maintainers. Getting feedback early in the process can help avoid this situation.

## Pull request reviews

Reviewing PRs requires time and attention, so we prioritize them as part of our regular sprint planning. The team works in fortnightly sprints, which means if you submit a PR early in the cycle, it might take some time before it’s reviewed. We understand this can be frustrating and strive to provide updates on the status of your PR as promptly as possible.

## Versioning and releases

We no longer rely on conventional commits, commitlint, or semantic-release. The version in `pyproject.toml` is the single source of truth and is bumped manually with [`uv version`](https://docs.astral.sh/uv/reference/cli/#uv-version).

To cut a new release:

1. On a release PR branch, bump the version with `uv`. Pick the bump type that matches the change:

   ```bash
   uv version --bump patch    # 1.3.1 -> 1.3.2 (bug fixes)
   uv version --bump minor    # 1.3.1 -> 1.4.0 (backwards-compatible features)
   uv version --bump major    # 1.3.1 -> 2.0.0 (breaking changes)
   ```

   This rewrites the `version = "..."` line in `pyproject.toml` and updates `uv.lock`.

2. Commit both files (`pyproject.toml` and `uv.lock`), open the PR, and merge it into `main` once approved.

3. Once the bump lands on `main`, the [`Release`](.github/workflows/release.yaml) workflow does everything in one shot: it compares `uv version --short` to the latest `v*` git tag, and if they differ it tags the commit and creates a GitHub Release with auto-generated notes, publishes the package to PyPI via [trusted publishing](https://docs.pypi.org/trusted-publishers/), deploys the versioned docs via `mike`, and pushes the production Docker image.

You should never tag or push releases by hand — the workflow does it from the bumped version on `main`. See [docs/docs/changelog.md](docs/docs/changelog.md) for the full job-by-job breakdown.
