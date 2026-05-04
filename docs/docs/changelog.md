# 📈 Releases & Changelog

Releases are cut from the `main` branch when the version in `pyproject.toml` changes. The version is bumped manually with [`uv version`](https://docs.astral.sh/uv/reference/cli/#uv-version) — `pyproject.toml` is the single source of truth.

## How to cut a release

1. On a release branch, bump the version with `uv`:

    ```bash
    uv version --bump patch    # 1.3.1 -> 1.3.2 (bug fixes)
    uv version --bump minor    # 1.3.1 -> 1.4.0 (backwards-compatible features)
    uv version --bump major    # 1.3.1 -> 2.0.0 (breaking changes)
    ```

2. Commit both `pyproject.toml` and `uv.lock`, open a PR, and merge to `main` once approved.

## What happens after merge

The [`Release`](https://github.com/populationgenomics/cpg-flow/blob/main/.github/workflows/release.yaml) workflow runs on every push to `main` and drives the entire release flow as a single workflow. Jobs are serialised so a failure short-circuits later, irreversible steps:

1. **`check-version`** compares `uv version --short` against the latest `v*` git tag. If they match, the rest of the workflow is skipped.
2. **`create-release`** runs `gh release create v<version> --generate-notes` to tag the commit and create a GitHub Release with auto-generated release notes.
3. **`push-docker`** builds the Docker image and pushes it to `australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:<version>`. Runs first so a Dockerfile or base-image breakage stops the release before PyPI sees the package.
4. **`publish-pypi`** runs `uv build --sdist --wheel` and publishes to PyPI via [trusted publishing](https://docs.pypi.org/trusted-publishers/) (`environment: production`). Only runs if the Docker image was built and pushed cleanly.
5. **`deploy-docs`** runs `mike deploy --push` to update the versioned docs on the `gh-pages` branch and point the `latest` alias at the new version. Only runs after both artefacts are published, so the `latest` alias never points at a release that doesn't exist on PyPI or in the Docker registry.

PR-time and manual Docker builds (dev images) still live in [`docker.yaml`](https://github.com/populationgenomics/cpg-flow/blob/main/.github/workflows/docker.yaml) and are unaffected by the release flow.

You should never tag or push releases by hand — the workflow does it from the bumped version on `main`.

Each change in a new release is listed in **<a href="https://github.com/populationgenomics/cpg-flow/blob/main/CHANGELOG.md" target="_blank">CHANGELOG.md</a>** (also generated from the GitHub Release notes).

## 🏷️ <a href="https://github.com/populationgenomics/cpg-flow/releases" target="_blank">All releases for this project are available here</a>.
