# Contribution Guidelines
This library was originally created by [Mark Hasegawa-Johnson](https://github.com/jhasegaw). This fork and the pypi package is maintained by [Virginia Partridge](https://github.com/ginic) with support from the [UMass Amherst Center for Data Science](https://ds.cs.umass.edu).

This is a community-driven, open source project that welcomes all contributions. Whether you're a seasoned contributor or new to the project, we're grateful for all contributions.

## Community standards
We are an inclusive community that values open dialogue, mutual respect, and fair treatment. Every submission will be treated equally and we encourage those with diverse backgrounds and perspectives to contribute.

As part of the University of Massachusetts Amherst, we adhere to the [UMass Code of Student Conduct](https://www.umass.edu/dean_students/codeofconduct).

## Getting started
Before contributing to the project, take a look at the README.md file, which contains information about installation and a project summary.

## Selecting an issue
Issues that are open for contribution are given the following labels:
- good-first-issue
  - Issues with this tag are suited for those that do not have previous experience with the project.
- help-wanted
  - Issues with this tag are open for contribution and are suited for those with experience in contribution.

## Issue reporting and help
Report bugs or suggested features as issues on the [Github repo](https://github.com/ginic/phonecodes). Check to see whether your problem has already been reported before creating a new issue. Please keep in mind that we are a small team with many responsibilities and may take awhile to respond.

# Development Guidelines
## Development environment set-up
To assist in maintaining code quality and software best practices, this project uses [pytest](https://docs.pytest.org) for unit tests and [ruff](https://github.com/astral-sh/ruff) as a code formatter and linter. You can set up your development environment by running `pip install -e .[dev,test]` from the root of the cloned repository on your computer. We recommend using a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) for development.

## Running unit tests
Once you have installed the `test` dependencies, unit tests can be run by calling `pytest` from the repository root. See the [pytest documentation](https://docs.pytest.org) for more details. Tests will also be run as a Github action when pull requests are opened or updated per `.github/workflows/python_package.yaml`

## Using ruff for linting and formatting
This project uses [ruff](https://docs.astral.sh/ruff/) to try to detect errors and format code. Once `dev` dependencies are installed, you can run checks with `ruff check <filepath>` or format files using `ruff format <filepath>`. Checks will also be run as a Github action when pull requests are opened per `.github/workflows/lint.yaml`

### Pre-commit hooks
An optional pre-commit configuration has been provided to run the ruff checks and formatter in `.pre-commit-config.yaml` to . To run checks as part of a git commit, [install pre-commit](https://pre-commit.com/#install) manually.

## Docstrings
The use of docstrings for documenting functions and modules is highly encouraged. Please use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

## Submitting contributions
To contribute to the project, do the following:
- [Fork and clone](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repository
- Create a [branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) for your issue and push your code changes to this branch.
- Make a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) to the main branch of the upstream repository
  - Note new changes under the "Unreleased" section in CHANGELOG.md
  - Make sure the unit tests pass on your branch. Maintainers will not approve code that fails tests.
  - Title your pull request with the issue you fixed
    - For example, "Fixed upload error to resolve Issue #987"
  - Include a short description of the changes you made

## Creating a release
For consistency, all version numbers for this project follow [semantic versioning](https://semver.org) with the format of integers A.B.C, where A is the “major” version, B is the “minor” version, and C is the “patch” version. Note that no version numbers should start with "v" anywhere, including on GitHub or in the CHANGELOG.md.

To create an official release, take the following steps:
1. Decide what the new version number will be according to semantic versioning principles.
2. Create a new branch from a commit that includes all the features and behavior that will be in the new version. On that branch, do the following:
    - Update the CHANGELOG.md with a section for the new version number and its release date. In that section list included features under the appropriate "Added", "Changed", and "Removed" headers.
    - Update the project version number in pyproject.toml
3. Create a pull request. Once the GitHub workflows for unit tests and publishing to TestPyPI pass, the pull request can be merged to the master branch.
4. Create an official release on GitHub following the [Creating a release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) from the merge commit in the previous step. Name and tag the release with your version number. Copy contents of the version's CHANGELOG.md section to the Release's description.
5. Validate that the GitHub workflow for publishing to PyPI passes and that the new version appears on https://pypi.org/project/phonecodes/#history.
