<!-- markdownlint-disable MD033 MD024 -->
# 🐙 CPG Flow

<img src="/assets/DNA_CURIOUS_FLOYD_CROPPED.png" height="300" alt="CPG Flow logo" align="right"/>

![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=2F73BF)

[![⚙️ Test Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)
[![🚀 Deploy To Production Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml)
[![GitHub release](https://img.shields.io/github/release/populationgenomics/cpg-flow.svg)](https://GitHub.com/populationgenomics/cpg-flow/releases/)
[![semantic-release: conventional commits](https://img.shields.io/badge/semantic--release-conventional%20commits-Æ1A7DBD?logo=semantic-release&color=1E7FBF)](https://github.com/semantic-release/semantic-release)
[![GitHub license](https://img.shields.io/github/license/populationgenomics/cpg-flow.svg)](https://github.com/populationgenomics/cpg-flow/blob/main/LICENSE)

[![Tests count](https://byob.yarr.is/populationgenomics/cpg-flow/test-badge)](https://byob.yarr.is/populationgenomics/cpg-flow/test-badge)
[![Coverage](https://byob.yarr.is/populationgenomics/cpg-flow/coverage-badge)](https://byob.yarr.is/populationgenomics/cpg-flow/coverage-badge)

[![Technical Debt](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=sqale_index&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Duplicated Lines (%)](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=duplicated_lines_density&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Code Smells](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=code_smells&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

<br />

## 📋 Table of Contents

1. 🐙 [What is this API ?](#what-is-this-api)
2. ✨ [Production and development links](#production-and-development-links)
3. 🔨 [Installation](#installation)
4. 🚀 [Build](#build)
5. 🐳 [Docker](#docker)
6. 💯 [Tests](#tests)
8. ☑️ [Code analysis and consistency](#code-analysis-and-consistency)
9. 📈 [Releases & Changelog](#versions)
10. 🎬 [GitHub Actions](#github-actions)
11. ✨ [Misc commands](#misc-commands)
12. ©️ [License](#license)
13. ❤️ [Contributors](#contributors)

## <a name="what-is-this-api">🐙 What is this API ?</a>

Welcome to CPG Flow!

This API provides a set of tools and workflows for managing population genomics data pipelines, designed to streamline the processing, analysis, and storage of large-scale genomic datasets. It facilitates automated pipeline execution, enabling reproducible research while integrating with cloud-based resources for scalable computation.

CPG Flow supports various stages of genomic data processing, from raw data ingestion to final analysis outputs, making it easier for researchers to manage and scale their population genomics workflows.

## <a name="production-and-development-links">✨ Production and development links</a>

### 🌐 Production

The production version of this API is documented at **[populationgenomics.github.io/cpg-flow](https://populationgenomics.github.io/cpg-flow/main/cpg_flow.html)**.

### 🛠️ Development

The development version of this API is available at **[populationgenomics.github.io/cpg-flow](https://populationgenomics.github.io/cpg-flow/alpha/cpg_flow.html)**.

The documentation is updated automatically when a commit is pushed on the `alpha` (prerelease) or `main` (release) branch.

## <a name="installation">🔨 Installation</a>

To install this project, you will need to have on your machine :

![PyPI](https://img.shields.io/badge/-PyPI-black?style=for-the-badge&logoColor=white&logo=pypi&color=3776AB)
![pip](https://img.shields.io/badge/-pip-black?style=for-the-badge&logoColor=white&logo=pip&color=3776AB)
![uv](https://img.shields.io/badge/-uv-black?style=for-the-badge&logoColor=white&logo=uv&color=3776AB)

To install this project, you will need to have Python and `pip` or `uv` installed on your machine.

We recommend using a virtual environment to manage your dependencies.

**If you don't have `uv` installed, you can still use `pip` for all commands below, but we recommend using `uv` for faster and more reliable installs.**

Then, run the following commands:

```bash
# Install the package using uv
uv sync

# Or equivalently
make init
```

Alternatively using pip
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the package using pip
pip install cpg-flow
```

### 🛠️ Development

To setup for development we recommend using the makefile setup
```bash
make init-dev
```

As this installs the pre-commit hooks for you. To install the local cpg-flow run
```bash
make install-local
```

You can also try out the pre-installed cpg-flow in our Docker, more information in the **[Docker section](#docker)**.

## <a name="build">🚀 Build</a>

To build the project, run the following command:

```bash
make build
```

To make sure that you're actually using the installed build we suggest calling the following to install the build wheel.

```bash
make install-build
```


## <a name="docker">🐳 Docker</a>

"""
## Docker Image Usage for cpg-flow Python Package

### Pulling and Using the Docker Image

These steps are restricted to CPG members only. Anyone will have access to the code in this public repositry and can build a version of cpg-flow themselves. The following requires authentication with the CPG's GCP.

To pull and use the Docker image for the `cpg-flow` Python package, follow these steps:

1. **Authenticate with Google Cloud Registry**:
    ```sh
    gcloud auth configure-docker australia-southeast1-docker.pkg.dev
    ```

2. **Pull the Docker Image**:
    - For alpha releases:
      ```sh
      docker pull australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:0.1.0-alpha.11
      ```
    - For main releases:
      ```sh
      docker pull australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:1.0.0
      ```

3. **Run the Docker Container**:
    ```sh
    docker run -it australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:<tag>
    ```

### Temporary Images for Development

Temporary images are created for each commit and expire in 30 days. These images are useful for development and testing purposes.

- Example of pulling a temporary image:
  ```sh
  docker pull australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow:991cf5783d7d35dee56a7ab0452d54e69c695c4e
  ```

### Accessing Build Images for CPG Members

Members of the CPG can find the build images in the Google Cloud Registry under the following paths:
- Alpha and main releases: `australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow`
- Temporary images: `australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow`

Ensure you have the necessary permissions and are authenticated with Google Cloud to access these images.


### 🧪 Unit and E2E tests

#### Unit Tests

[![Tests count](https://byob.yarr.is/populationgenomics/cpg-flow/test-badge)](https://byob.yarr.is/populationgenomics/cpg-flow/test-badge)

[![Coverage](https://byob.yarr.is/populationgenomics/cpg-flow/coverage-badge)](https://byob.yarr.is/populationgenomics/cpg-flow/coverage-badge)


#### E2E Test

We recommend frequently running the manual test workflow found in [test_workflows_shared](https://github.com/populationgenomics/test_workflows_shared)  specifically the `cpg_flow_test` workflow during development to ensure updates work with the CPG production environment.

Docummentation for running the tests are found in the repository readme.


### ▶️ Commands

Before testing, you must follow the **[installation steps](#installation)**.

## <a name="code-analysis-and-consistency">☑️ Code analysis and consistency</a>

### 🔍 Code linting & formatting

![Precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

In order to keep the code clean, consistent and free of bad python practices, more than **Over 10 pre-commit hooks are enabled** !

Complete list of all enabled rules is available in the **[.pre-commit-config.yaml file](https://github.com/populationgenomics/cpg-flow/blob/main/.pre-commit-config.yaml)**.

### ▶️ Commands

Before linting, you must follow the [installation steps](#installation).

Then, run the following command

```bash
# Lint
pre-commit run --all-files
```

When setting up local linting for development you can also run the following once:

```bash
# Install the pre-commit hook
pre-commit install

# Or equivalently
make init || make init-dev
```

### 🥇 Project quality scanner

Multiple tools are set up to maintain the best code quality and to prevent vulnerabilities:

![SonarQube](https://img.shields.io/badge/-SonarQube-black?style=for-the-badge&logoColor=white&logo=sonarqube&color=4E9BCD)

SonarQube summary is available **[here](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)**.

[![Coverage](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=coverage&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Duplicated Lines (%)](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=duplicated_lines_density&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Quality Gate Status](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=alert_status&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

[![Technical Debt](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=sqale_index&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Vulnerabilities](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=vulnerabilities&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Code Smells](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=code_smells&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

[![Reliability Rating](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=reliability_rating&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Security Rating](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=security_rating&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Bugs](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=bugs&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)


## <a name="versions">📈 Releases & Changelog</a>

Releases on **main** branch are generated and published automatically,
pre-releases on the **alpha** branch are also generated and published by:

![Semantic Release](https://img.shields.io/badge/-Semantic%20Release-black?style=for-the-badge&logoColor=white&logo=semantic-release&color=000000)

It uses the **[conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)** strategy.

Each change when a new release comes up is listed in the **<a href="https://github.com/populationgenomics/cpg-flow/blob/main/CHANGELOG.md" target="_blank">CHANGELOG.md file</a>**.

Also, you can keep up with changes by watching releases via the **Watch GitHub button** at the top of this page.

#### 🏷️ <a href="https://github.com/populationgenomics/cpg-flow/releases" target="_blank">All releases for this project are available here</a>.

## <a name="github-actions">🎬 GitHub Actions</a>

This project uses **GitHub Actions** to automate some boring tasks.

You can find all the workflows in the **[.github/workflows directory](https://github.com/populationgenomics/cpg-flow/tree/main/.github/workflows).**

### 🎢 Workflows

| Name | Description & Status | Triggered on |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------: |
| **[Renovate](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml)** | Runs Renovate to update dependencies.<br/><br/>[![Renovate](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml) | `schedule` and `workflow_dispatch` |
| **[Test](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)** | Runs unit tests and generates coverage reports.<br/><br/>[![Test](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml) | `push` |
| **[Security Checks](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml)** | Performs security checks using pip-audit.<br/><br/>[![Security Checks](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml) | `workflow_dispatch` and `push` |
| **[Deploy API Documentation](https://github.com/populationgenomics/cpg-flow/actions/workflows/web_docs.yaml)** | Deploys API documentation to GitHub Pages.<br/><br/>[![Deploy API Documentation](https://github.com/populationgenomics/cpg-flow/actions/workflows/web_docs.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/web_docs.yaml) | `push` and `workflow_dispatch` |
| **[Package](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml)** | Packages the project and publishes it to PyPI and GitHub Releases.<br/><br/>[![Package](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml) | `workflow_dispatch` and `push` on `alpha, main` |
| **[Lint](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml)** | Runs linting checks using pre-commit hooks.<br/><br/>[![Lint](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml) | `push` |
| **[Docker](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml)** | Builds and pushes Docker images for the project.<br/><br/>[![Docker](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml) | `pull_request` on `main, alpha` and `push` on `main, alpha` and `workflow_dispatch` |


## <a name="misc-commands">✨ Misc commands</a>

TODO

<!--
### 🌳 Animated tree visualisation of the project's evolution with **[Gource](https://gource.io/)**
```shell
# Please ensure that `gource` is installed on your system.
pnpm run gource
```

### 🔀 Create git branch with a conventional name
```shell
pnpm run script:create-branch
```

### ⤴️ Create pull request against the `develop` branch from current branch
```shell
pnpm run script:create-pull-request
```

### 📣 To all IntelliJ IDEs users (IntelliJ, Webstorm, PHPStorm, etc.)

All the above commands are available in the **.run directory** at the root of the project.

You can add them as **run configurations** in your IDE.

-->

## <a name="license">©️ License</a>

This project is licensed under the [MIT License](http://opensource.org/licenses/MIT).

## <a name="contributors">❤️ Contributors</a>

There is no contributor yet. Want to be the first ?

If you want to contribute to this project, please read the [**contribution guide**](https://github.com/populationgenomics/cpg-flow/blob/master/CONTRIBUTING.md).
