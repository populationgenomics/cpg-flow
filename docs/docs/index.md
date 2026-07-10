<!-- markdownlint-disable MD033 MD024 -->
# 🐙 CPG Flow

<img src="assets/DNA_CURIOUS_FLOYD_CROPPED.png" alt="CPG Flow logo" align="center"/>

![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=2F73BF)

[![⚙️ Test Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)
[![🚀 Release Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/release.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/release.yaml)
[![GitHub Latest Main Release](https://img.shields.io/github/v/release/populationgenomics/cpg-flow?label=main%20release)](https://GitHub.com/populationgenomics/cpg-flow/releases/)
[![GitHub Release](https://img.shields.io/github/v/release/populationgenomics/cpg-flow?include_prereleases&label=latest)](https://GitHub.com/populationgenomics/cpg-flow/releases/)
[![GitHub license](https://img.shields.io/github/license/populationgenomics/cpg-flow.svg)](https://github.com/populationgenomics/cpg-flow/blob/main/LICENSE)


![Tests](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fpopulationgenomics%2Fcpg-flow%2Frefs%2Fheads%2FSET-328-README-prioritises-pipelines-instead-of-framework%2Fdocs%2Fbadges.yaml&query=%24.test-badge.status&label=Tests&color=%24.test-badge.color)
![Coverage](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fpopulationgenomics%2Fcpg-flow%2Frefs%2Fheads%2FSET-328-README-prioritises-pipelines-instead-of-framework%2Fdocs%2Fbadges.yaml&query=%24.coverage-badge.status&label=Coverage&color=%24.coverage-badge.color)


[![Technical Debt](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=sqale_index&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Duplicated Lines (%)](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=duplicated_lines_density&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Code Smells](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=code_smells&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

<br />

## 📋 Table of Contents

1. 🐙 [What is this API ?](#what-is-this-api)
2. ✨ [Documentation](#documentation)
3. 🔨 [Installation](installation.md#installation)
4. 🚀 [Build](installation.md#build)
5. 🤖 [Usage](usage.md#usage)
6. 😵‍💫 [Key Considerations and Limitations](considerations-limitations.md#key-considerations-and-limitations)
7. 🐳 [Docker](docker.md#docker)
8. 💯 [Tests](tests.md#unit-and-e2e-tests)
9. ☑️ [Code analysis and consistency](code-analysis-consistency.md#code-linting-and-formatting)
10. 📈 [Releases & Changelog](changelog.md)
11. 🎬 [GitHub Actions](workflows.md#github-actions)

## <a name="what-is-this-api">🐙 What is this API ?</a>

Welcome to CPG Flow!

This API provides a set of tools and workflows for managing population genomics data pipelines, designed to streamline the processing, analysis, and storage of large-scale genomic datasets. It facilitates automated pipeline execution, enabling reproducible research while integrating with cloud-based resources for scalable computation.

CPG Flow supports various stages of genomic data processing, from raw data ingestion to final analysis outputs, making it easier for researchers to manage and scale their population genomics workflows.

The API constructs a DAG (Directed Acyclic Graph) structure from a set of chained stages. This DAG structure then forms the **pipeline**.

## <a name="documentation">✨ Documentation</a>

### 🌐 Production

The production version of this API is documented at **[populationgenomics.github.io/cpg-flow/](https://populationgenomics.github.io/cpg-flow/)**.

The documentation is updated automatically by the Release workflow when a new version is cut from `main`. Older versions remain accessible via the version selector (powered by [`mike`](https://github.com/jimporter/mike)).
