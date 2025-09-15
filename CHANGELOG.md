# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

You should also add project tags for each release in Github, see [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

# [Unreleased]

# [1.2.1] - 9/15/2025
### Changed
- Updated TIMIT conversions to IPA to use syllabic diacritics, mapping 'ER' to 'ɹ̩' and 'ENG' to 'ŋ̩'

# [1.2.0] - 6/23/2025
### Changed
- Improved error messages about limited support for TIMIT

### Fixed
- TestPyPI GitHub workflow ignores existing release numbers, so job doesn't fail when version numbers are re-used
- Corrected handling of stop closure symbols in TIMIT and made TIMIT to IPA conversion more robust to variation in transcriptions of stop/affricates

# [1.1.4] - 11/14/2024
### Changed
- Remove GitHub release action from release GitHub workflow, as it doesn't work with the release structure laid out in CONTRIBUTIONS.md

# [1.1.3] - 11/14/2024
### Changed
- Version bump due to PyPI issues. You cannot re-upload artifacts even if they are deleted.

# [1.1.2] - 11/13/2024
### Added
- Support for the bilabial fricative mapping between Buckeye (BF) and IPA (β)
- Release creation instructions to CONTRIBUTIONS.md

### Changed
- Updated GitHub actions to latest 3.0.0 version of sigstore/gh-action-sigstore-python

# [1.1.1] - 5/9/2024
### Added
- Compatibility with older version of python back to 3.7

### Changed
- Updated Github actions to latest version per warning about Node.js 16 version being deprecated

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