# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

You should also add project tags for each release in Github, see [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

# [1.1.1] - 5/9/2024
### Added
- Compatibility with older version of python back to 3.7

# [1.1.0] - 2/12/2024
### Added
- Support for converting between the Buckeye corpus phonetic alphabet and IPA

### Changed
- Made language explicitly optional for conversions between ARPABET and X-SAMPA
- Minor updates to README and CONTRIBUTIONS

# [1.0.0] - 2/9/2024
### Added
- Modern python packaging, including pyproject.toml
- Contribution guidelines
- Changelog with sematic versioning
- Usage examples in README
- Unit tests using pytest and triggered by Github Action on pull request
- Checks and linting with Ruff

### Changed
- Ordering of language and corpus code in phonecodes.pronlex.read
- Removed duplicated dictionary keys in phonecodes.phonecode_tables

### Removed

# [0.0.0] - 2020
### Added
- Initial repository created by https://github.com/jhasegaw