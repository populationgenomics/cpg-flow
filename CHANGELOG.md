# CHANGELOG


## v0.0.1-alpha.2 (2024-10-30)

### Bug Fixes

* fix(package.yaml): typo in token name TEST_PYPI_API_TOKEN ([`2ab5be4`](https://github.com/populationgenomics/cpg-flow/commit/2ab5be4e987e2c936e287d74dfae2543a599ea8f))

* fix(package.yaml): typo in semantic release command ([`b480575`](https://github.com/populationgenomics/cpg-flow/commit/b480575c7d7732dae92639f937b1ff23e92e45a8))

### Continuous Integration

* ci(package.yaml): split semantic version and publish ([`8c04d34`](https://github.com/populationgenomics/cpg-flow/commit/8c04d3434f93800009aa0b76d3780d4953c81ce2))

* ci(package.yaml): fix requirements and add pypi token ([`2bb89f7`](https://github.com/populationgenomics/cpg-flow/commit/2bb89f766d0422786df53fe5593e59d355ba7586))

* ci(package.yaml): switch to semantic release ([`891da2c`](https://github.com/populationgenomics/cpg-flow/commit/891da2cb20f7d59bf115b504a2a37d251d18a0f6))


## v0.0.1-alpha.1 (2024-10-30)

### Bug Fixes

* fix(semantic-release): add build command ([`34bdc9a`](https://github.com/populationgenomics/cpg-flow/commit/34bdc9ad69236f7eb19411edf799f04c3db13dc3))

* fix(semantic-release): prefix the release message with "bump: " ([`73bf215`](https://github.com/populationgenomics/cpg-flow/commit/73bf2151379e660f07c77cb17a1e46d05b26e53a))

* fix(pyproject.toml): change prerelease tag from pre to alpha ([`fe393c5`](https://github.com/populationgenomics/cpg-flow/commit/fe393c5e201212765b467a623b1b21dee8351e1b))

* fix: update package.yaml to use semantic release ([`a22c8be`](https://github.com/populationgenomics/cpg-flow/commit/a22c8be0396920f1550b60c05cc7e85911281d4e))

* fix(pyproject.toml): setting up prerelease branch config ([`79f774e`](https://github.com/populationgenomics/cpg-flow/commit/79f774ec7bc7696da9015dd8169ace66ec416a66))

* fix(pyproject.toml): switch back to 3.10 for prod pipes, add deps fix ([`1a0e214`](https://github.com/populationgenomics/cpg-flow/commit/1a0e2144901697029f1196cc8bedc9ab7979542e))

* fix(test.yaml): fix path to tests folder ([`199b168`](https://github.com/populationgenomics/cpg-flow/commit/199b1684974159b7afa1b5c6e33decdecaad4505))

* fix(test.yaml): revert to 3.10 ([`69e4f14`](https://github.com/populationgenomics/cpg-flow/commit/69e4f14d8f9dd1341021ce6ddad1a30542797ef5))

### Build System

* build(.gitignore): remove redundant inclusion of .pypirc ([`92c5a7a`](https://github.com/populationgenomics/cpg-flow/commit/92c5a7a844f80164d4a9abfd7f2497880803e473))

* build: setup pyproject and Makefile to build upload to pypi ([`16cd9e7`](https://github.com/populationgenomics/cpg-flow/commit/16cd9e7053373264cadc2b2e4216c3e0b500b0cd))

* build(Makefile,README.md): update dev instructions and init in Makefile ([`ff111d8`](https://github.com/populationgenomics/cpg-flow/commit/ff111d831c4aa3527fe47bc9d38b14988dcabd24))

* build(test.yaml): disable test workflow for now ([`3574ea2`](https://github.com/populationgenomics/cpg-flow/commit/3574ea2621cd5b23f1214ca0740d9e3cabbea8cc))

* build(pre-commit): add commitlint ([`09c6915`](https://github.com/populationgenomics/cpg-flow/commit/09c691512273b6ebd519c83da756f4dd0fffe096))

* build(Makefile): create makefile for building and installing dependencies ([`b8ab07b`](https://github.com/populationgenomics/cpg-flow/commit/b8ab07bc6133a054bb9ed531fc055fc0f31f3a90))

### Code Style

* style(README): fix title links ([`54e8031`](https://github.com/populationgenomics/cpg-flow/commit/54e8031cbb82b252a016d5a3a19cf6ab24e85388))

### Continuous Integration

* ci(.github/workflows/package.yaml): Changed the package name to cpg_flow ([`6d0c053`](https://github.com/populationgenomics/cpg-flow/commit/6d0c053a770ed54fb2564e18129077b90782fb61))

### Refactoring

* refactor(.files,-pyproject.toml,-__init__.py,-README.md): Added config files and update to readme ([`1fd7ae6`](https://github.com/populationgenomics/cpg-flow/commit/1fd7ae69dfafc6a58435723d14a4a452822d5e0a))

### Unknown

* added renovate config ([`bb4ec9e`](https://github.com/populationgenomics/cpg-flow/commit/bb4ec9eba4ed1dd9aa9e10892b527171b5346e8d))

* Merge pull request #2 from populationgenomics/add-workflows

Add workflows ([`4615999`](https://github.com/populationgenomics/cpg-flow/commit/4615999b2a012227d71eec3a139391baf4dd2d46))

* chore: merge remote ([`10149d5`](https://github.com/populationgenomics/cpg-flow/commit/10149d58a66244a30390065c250c1c083fbb34f8))

* revert pre-commit to 3.10 ([`feae06d`](https://github.com/populationgenomics/cpg-flow/commit/feae06d56abc98abfec8feac7f9d85174515d0e0))

* merge from main ([`d60aa1d`](https://github.com/populationgenomics/cpg-flow/commit/d60aa1d8a519b34ad877dfaf3a5ead382e7ab694))

* chore: merge main ([`0fb19d8`](https://github.com/populationgenomics/cpg-flow/commit/0fb19d8a3b512367c2f0f131244510e271a66006))

* Merge pull request #3 from populationgenomics/add-renovate

Add RenovateBot ([`aaab653`](https://github.com/populationgenomics/cpg-flow/commit/aaab653347f76484513951fce6e72a8f70dfc10e))

* bump lint python to 3.12 ([`23123c8`](https://github.com/populationgenomics/cpg-flow/commit/23123c811998ff93e1024469e7e34822a078e4e3))

* added lint ignore for readme ([`b1ed388`](https://github.com/populationgenomics/cpg-flow/commit/b1ed388f5055b3c6c586e7ff2f9703e1e7e30c99))

* added renovate config ([`8a32997`](https://github.com/populationgenomics/cpg-flow/commit/8a329976b3132492e4f78fb3e0b5a6ff8cd30a45))

* Updates ([`4f6a386`](https://github.com/populationgenomics/cpg-flow/commit/4f6a38696413ff0f04926ff0fb56dc6cab91a219))

* Updates ([`9db3681`](https://github.com/populationgenomics/cpg-flow/commit/9db3681ab0f9bbb0044eb96d26be142ead03fa1c))

* Re add pyproject.toml ([`bd2d7b4`](https://github.com/populationgenomics/cpg-flow/commit/bd2d7b44bee2f2cf8ca2aed5de559e86580d9af5))

* Add test and lint file requirements ([`b3de936`](https://github.com/populationgenomics/cpg-flow/commit/b3de936908dc2a3dd4ef88d0aea70df89e528500))

* Add test and lint file requirements ([`53c19ab`](https://github.com/populationgenomics/cpg-flow/commit/53c19ab7db1b88f84f260a61f3b539d1c475f545))

* Update README.md ([`c954b30`](https://github.com/populationgenomics/cpg-flow/commit/c954b3064fb4eb5cbf12834637f8c0a87189da78))

* Template README.md ([`f2dd4aa`](https://github.com/populationgenomics/cpg-flow/commit/f2dd4aafa9d6aa67b6f5f63342a0c4a1386f78b3))

* Add DNA Floyd ([`3d35bb7`](https://github.com/populationgenomics/cpg-flow/commit/3d35bb708b8c06526ca1032bf0dfebfc2fa5608a))

* added initial repo md files ([`0bd3aa1`](https://github.com/populationgenomics/cpg-flow/commit/0bd3aa12544267c39461b53d01ad2c1689ac990e))

* Initial commit ([`6e306e6`](https://github.com/populationgenomics/cpg-flow/commit/6e306e653abc203f5f55bc6ecb601da8147ce3cb))
