# Changelog

## Unreleased (2025-12-20)

## v0.8.5 (2025-12-20)

### Other

- Bump version: 0.8.4 → 0.8.5.
    
- Chore: add duty as dev.
    
- Chore: adjust tasks.
    
- Bump version: 0.8.3 → 0.8.4.
    
- Docs: Comprehensive Documentation Improvements.
    
  This PR includes a series of improvements to the Sphinx documentation and its build process:

  - Adds a "View on GitHub" link to the documentation, making it easier for users to navigate to the source code repository.
  - Updates the copyright notice in the documentation footer to include the current year and the author's name.
  - Automates changelog generation for both local and CI/CD documentation builds, ensuring the changelog is always up-to-date.
  - Updates the CI/CD workflow for documentation to use the correct build task.
### Updates

- Refactor: Align tasks with duties and fix version bumping.
    
## v0.8.3 (2025-12-20)

## v0.8.4 (2025-12-17)

### Other

- Bump version: 0.8.3 → 0.8.4.
    
- Docs: Comprehensive Documentation Improvements.
    
  This PR includes a series of improvements to the Sphinx documentation and its build process:

  - Adds a "View on GitHub" link to the documentation, making it easier for users to navigate to the source code repository.
  - Updates the copyright notice in the documentation footer to include the current year and the author's name.
  - Automates changelog generation for both local and CI/CD documentation builds, ensuring the changelog is always up-to-date.
  - Updates the CI/CD workflow for documentation to use the correct build task.
- Bump version: 0.8.2 → 0.8.3.
    
- Docs: Add repository link and update copyright in Sphinx docs.
    
  - Adds a "Edit on GitHub" link to each page in the Sphinx documentation, pointing to the corresponding source file in the repository.
  - Updates the copyright notice in the documentation footer to include the current year and the author's name.
- Bump version: 0.8.1 → 0.8.2.
    
## v0.8.2 (2025-11-02)

### Fixes

- Fix(api): Correctly format SMW API parameters.
    
  - Modifies the `AskEndpoint.execute` method to correctly append
    parameters like `limit`, `sort`, and `offset` to the main query string,
    separated by pipes (`|`), as expected by the Semantic MediaWiki API.
  - Removes the incorrect and non-functional `p_` prefix convention for
    special parameters.
  - Updates tests to verify the new, correct query string format.
  - Updates `EXAMPLES.md` to remove the incorrect `p_` prefix
    documentation and provide accurate examples for passing parameters.
### Other

- Bump version: 0.8.1 → 0.8.2.
    
- Bump version: 0.8.0 → 0.8.1.
    
## v0.8.1 (2025-11-02)

### Other

- Bump version: 0.8.0 → 0.8.1.
    
- Docs: add example for p_ parameter.
    
  Adds an example to EXAMPLES.md to demonstrate how to use p_ prefixed keyword arguments to pass special parameters to the 'Special:Ask' API.
- Bump version: 0.7.11 → 0.8.0.
    
## v0.8.0 (2025-11-02)

### Other

- Bump version: 0.7.11 → 0.8.0.
    
- Feat(ask): Add support for special 'p' parameters.
    
  This commit introduces a feature that allows passing special 'ask' parameters, like `p[limit]`, by using keyword arguments prefixed with `p_`. The `AskEndpoint` now correctly formats these arguments into the `p[key]` format required by the Semantic MediaWiki API.

  A test case has been added to verify this functionality.
- Bump version: 0.7.10 → 0.7.11.
    
## v0.7.11 (2025-10-27)

### Other

- Bump version: 0.7.10 → 0.7.11.
    
## v0.0.1 (2025-10-27)

### Fixes

- Fix(workflows): consolidate release and publish workflows.
    
  Consolidate the release and publish workflows into a single workflow to prevent conflicts and ensure that the publish step runs reliably after a tag is pushed.
### Other

- Bump version: 0.7.9 → 0.7.10.
    
## v0.7.10 (2025-10-27)

### Other

- Bump version: 0.7.9 → 0.7.10.
    
- Feat: Add PyPI publish workflow.
    
  This commit adds a new GitHub Actions workflow to publish the package to PyPI. The workflow is triggered when a new tag is pushed to the repository. It uses trusted publishing to securely authenticate with PyPI.
- Bump version: 0.7.8 → 0.7.9.
    
## v0.7.9 (2025-10-27)

### Other

- Bump version: 0.7.8 → 0.7.9.
    
- Bump version: 0.7.7 → 0.7.8.
    
### Updates

- Update the installation instructions in the README.md to use 'uv add' instead of 'uv pip install'. This reflects the preferred modern usage of the uv package manager.
    
## v0.7.8 (2025-10-26)

### Fixes

- Fix: Correct release workflow to build artifacts.
    
### Other

- Bump version: 0.7.7 → 0.7.8.
    
- Bump version: 0.7.6 → 0.7.7.
    
## v0.7.7 (2025-10-26)

### Fixes

- Fix: show version below title in docs.
    
- Fix(docs): correctly display project name and version in Sphinx docs.
    
  This change modifies the Sphinx configuration to correctly display the project name and version in the top-left corner of the documentation, improving visibility and branding.

  A custom HTML template is used to override the theme's default navigation branding and insert the version number below the project name. This is necessary because the `display_version` theme option is deprecated and there is no direct replacement.
- Fix: Ensure Sphinx displays version from pyproject.toml.
    
  This commit resolves an issue where the project version, intended to be sourced from `pyproject.toml` via the `sphinx-pyproject` extension, was not being displayed in the generated Sphinx documentation.

  The root cause was a misconfiguration in `docs/sphinx/conf.py`. The `myst_substitutions` dictionary was being defined before `sphinx-pyproject` had the opportunity to inject the `version` and `release` variables into the configuration's global namespace, leading to a `NameError` during the Sphinx build process.

  The fix involves two key changes:
  1.  The `myst_substitutions` block is moved to the end of `conf.py` to ensure it executes after `sphinx-pyproject` has populated the `version` variable.
  2.  Since `sphinx-pyproject` only defines `version`, the `release` key in the dictionary is also set to use the `version` variable.
  3.  `# noqa: F821` comments have been added to suppress linter warnings about the dynamically injected `version` variable being undefined at static analysis time.
- Fixes an issue where the package version was not being displayed in the Sphinx documentation.
    
  The `sphinx-pyproject` extension updates the Sphinx configuration variables (`version` and `release`) during the `config-inited` event. This event occurs after the `conf.py` file has been fully executed.

  The previous implementation attempted to access these variables at the top level of `conf.py`, which resulted in them being undefined.

  This change defers the population of `myst_substitutions` until after `sphinx-pyproject` has updated the configuration by connecting a function to the `config-inited` event.
### Other

- Bump version: 0.7.6 → 0.7.7.
    
- Chore: add version to docs.
    
- Bump version: 0.7.5 → 0.7.6.
    
### Updates

- Refactor: Dynamically set project name in Sphinx conf.py.
    
  This commit refactors the Sphinx configuration to dynamically set the project name from `pyproject.toml` using `sphinx-pyproject`. This removes the hardcoded project name and ensures that the documentation stays in sync with the project's metadata.

  The change was verified by building and serving the documentation locally.
## v0.7.6 (2025-10-25)

### Fixes

- Fix: documentation.
    
  add query builder examples
### Other

- Bump version: 0.7.5 → 0.7.6.
    
- Bump version: 0.7.4 → 0.7.5.
    
## v0.7.5 (2025-10-25)

### Other

- Bump version: 0.7.4 → 0.7.5.
    
- Docs: Add example for advanced queries.
    
  Adds a new section to the `README.md` file to explain and provide an example for using dictionary-based conditions in the `QueryBuilder`. This documents the existing, but previously undocumented, functionality of using operators for more complex queries, such as date comparisons.
- Bump version: 0.7.3 → 0.7.4.
    
- Chore: uodate changelog.
    
- Docs: extend QueryBuilder usage examples.
    
  The usage examples for the QueryBuilder were a bit thin. This change extends the usage examples with more advanced cases. It now shows valid comparison operators for dates and select examples valid for the smw ask query syntax.
## v0.7.3 (2025-10-20)

### Other

- Bump version: 0.7.2 → 0.7.3.
    
- Feat(docs): add EXAMPLES.md to Sphinx build.
    
  Adds a new `EXAMPLES.md` file to the Sphinx documentation, providing usage examples for the `AskEndpoint` and `QueryBuilder`.

  - Creates `docs/sphinx/EXAMPLES.md` with detailed code examples.
  - Integrates the new file into the Sphinx `toctree` in `docs/sphinx/index.md`.
  - Verifies the documentation build to ensure the new page is included correctly.
- Bump version: 0.7.1 → 0.7.2.
    
## v0.7.2 (2025-10-20)

### Fixes

- Fix: drop old file.
    
### Other

- Bump version: 0.7.1 → 0.7.2.
    
- Bump version: 0.7.0 → 0.7.1.
    
## v0.7.1 (2025-10-20)

### Fixes

- Fix: imports.
    
### Other

- Bump version: 0.7.0 → 0.7.1.
    
- Bump version: 0.6.26 → 0.7.0.
    
## v0.7.0 (2025-10-20)

### Other

- Bump version: 0.6.26 → 0.7.0.
    
- Feat: add query composition.
    
- Feat: Reimplement QueryBuilder for complex queries.
    
  Reimplements the `QueryBuilder` to support complex queries from dictionaries.

  This change restores the ability to build complex queries like `[[Intro-Date::>{{#time:2020-10-10}}]]` from a dictionary containing a key, an optional operator, and a value.

  The `add_conditions` method now accepts both strings and dictionaries.
  The `build` method has been updated to correctly join multiple conditions.

  A dedicated test file for the `QueryBuilder` has been added, with comprehensive tests for the new functionality.
- Bump version: 0.6.25 → 0.6.26.
    
## v0.6.26 (2025-10-20)

### Other

- Bump version: 0.6.25 → 0.6.26.
    
- Chore: add release action.
    
- Bump version: 0.6.24 → 0.6.25.
    
## v0.6.25 (2025-10-20)

### Fixes

- Fix: QueryBuilder import.
    
### Other

- Bump version: 0.6.24 → 0.6.25.
    
- Bump version: 0.6.23 → 0.6.24.
    
## v0.6.24 (2025-10-20)

### Fixes

- Fix: tags.
    
### Other

- Bump version: 0.6.23 → 0.6.24.
    
- Bump version: 0.6.22 → 0.6.23.
    
## v0.6.23 (2025-10-20)

### Other

- Bump version: 0.6.22 → 0.6.23.
    
- Bump version: 0.6.21 → 0.6.22.
    
- Bump version: 0.6.20 → 0.6.21.
    
## v0.6.21 (2025-10-20)

### Fixes

- Fix: expose QueryBuilder.
    
### Other

- Bump version: 0.6.20 → 0.6.21.
    
- Bump version: 0.6.19 → 0.6.20.
    
## v0.6.20 (2025-10-20)

### Fixes

- Fix: align bump-my-version and generate-changelog configurations.
    
### Other

- Bump version: 0.6.19 → 0.6.20.
    
- Build: stop tracking uv.lock.
    
- Build: ignore uv.lock.
    
### Updates

- Refactor: use post-commit hook for changelog generation.
    
- Refactor: simplify release process.
    
## v0.6.22 (2025-10-20)

### Fixes

- Fix: taskfile version commands.
    
### Other

- Bump version: 0.6.21 → 0.6.22.
    
- Chore: configure bump-my-version to trigger generate-changelog.
    
## v0.6.19 (2025-10-20)

### Fixes

- Fix: update changelog and release tasks.
    
- Fix: add changelog to bump.
    
### Other

- Bump version: 0.6.18 → 0.6.19.
    
- Bump version: 0.6.16 → 0.6.17.
    
## v0.6.17 (2025-10-20)

### Other

- Bump version: 0.6.16 → 0.6.17.
    
- Chore: update uv.lock.
    
## v0.6.16 (2025-10-20)

### Fixes

- Fix: track uv lock on bump.
    
- Fix: writing changelog.
    
### Other

- Bump version: 0.6.15 → 0.6.16.
    
- Feat: configure changelog and release tasks.
    
## v0.6.14 (2025-10-20)

### Fixes

- Fix: format.
    
### Other

- Bump version: 0.6.13 → 0.6.14.
    
- Docs(changelog): Update changelog and document missing entries.
    
  Updates the CHANGELOG.md to include the changes for version 0.6.13. This version includes a refactoring of the AskEndpoint to remove deprecated methods and focus on the QueryBuilder.

  Also adds a note to the changelog to explain that the entries for versions 0.1.2 to 0.6.12 were not recorded.
## v0.6.13 (2025-10-19)

### Fixes

- Fix: uv version in ci-cd.
    
### Other

- Bump version: 0.6.12 → 0.6.13.
    
## v0.6.12 (2025-10-19)

### Fixes

- Fix: use uv.
    
### Other

- Bump version: 0.6.11 → 0.6.12.
    
## v0.6.11 (2025-10-19)

### Fixes

- Fix: online docs.
    
### Other

- Bump version: 0.6.10 → 0.6.11.
    
## v0.6.10 (2025-10-19)

### Fixes

- Fix: docu.
    
### Other

- Bump version: 0.6.9 → 0.6.10.
    
## v0.6.9 (2025-10-19)

### Other

- Bump version: 0.6.8 → 0.6.9.
    
- Chore: bump deps.
    
## v0.6.8 (2025-10-19)

### Fixes

- Fix: centralized version.
    
### Other

- Bump version: 0.6.7 → 0.6.8.
    
## v0.6.7 (2025-10-19)

### Fixes

- Fix: coverage output.
    
### Other

- Bump version: 0.6.6 → 0.6.7.
    
## v0.6.6 (2025-10-19)

### Fixes

- Fix: duties.
    
### Other

- Bump version: 0.6.5 → 0.6.6.
    
- Docs: Replace FRITZ!Box example with FSF SMW.
    
  Replaced all instances of the "FRITZ!Box" example in the documentation with a more appropriate example from the Free Software Foundation's Semantic MediaWiki.

  - Replaced "FRITZ!Box-Family" with "Free-Software".
  - Replaced "Intro-Date" with "Modification date".

  **note:** Due to network connectivity issues from the execution environment, I was unable to verify the FSF SMW endpoint and its properties. The property "Modification date" was chosen as a likely candidate, but this could not be confirmed. I was also unable to find any other occurrences of "FRITZ!Box" in the codebase.

## v0.6.5 (2025-10-19)

### Fixes

- Fix: icon.
    
### Other

- Bump version: 0.6.4 → 0.6.5.
    
## v0.6.4 (2025-10-19)

### Fixes

- Fix: svg.
    
### Other

- Bump version: 0.6.3 → 0.6.4.
    
- Feat: Add favicon to Sphinx documentation.
    
  This commit adds a custom SVG favicon to the Sphinx documentation.

  A new SVG icon has been created and placed in the 'docs/sphinx/_static' directory. The Sphinx configuration file 'docs/sphinx/conf.py' has been updated to use this new favicon.
## v0.6.3 (2025-10-19)

### Fixes

- Fix: include smw syntax info.
    
### Other

- Bump version: 0.6.2 → 0.6.3.
    
## v0.6.2 (2025-10-19)

### Fixes

- Fix: resore files.
    
### Other

- Bump version: 0.6.1 → 0.6.2.
    
## v0.6.1 (2025-10-19)

### Fixes

- Fix: use sphinx for documentation.
    
- Fix(docs): correct mkdocstrings path in mkdocs.yml.
    
  This change corrects the `mkdocstrings` configuration in `mkdocs.yml` to correctly point to the `src` directory. This resolves the `ModuleNotFoundError` that was occurring in the CI build.
### Other

- Bump version: 0.6.0 → 0.6.1.
    
- Chore: stop tracking generated site/ directory.
    
- Chore: expand .gitignore for caches, site and IDE files.
    
- Bump version: 0.5.1 → 0.6.0.
    
- Feat(docs): switch to mkdocs for documentation.
    
  This change replaces pdoc with MkDocs as the documentation generator.

  This allows for the inclusion of existing markdown files (like the README and CHANGELOG) alongside the API documentation, which is generated from the Python docstrings using the mkdocstrings plugin.

  The GitHub Actions workflow has been updated to use MkDocs, and the documentation has been restructured to support the new format.
## v0.5.1 (2025-10-18)

### Fixes

- Fix: docs streamlined.
    
### Other

- Bump version: 0.5.0 → 0.5.1.
    
## v0.5.0 (2025-10-18)

### Other

- Bump version: 0.4.2 → 0.5.0.
    
- Feat: move syntax info md into docs.
    
## v0.4.2 (2025-10-18)

### Fixes

- Fix: pdoc command.
    
### Other

- Bump version: 0.4.1 → 0.4.2.
    
## v0.4.1 (2025-10-18)

### Fixes

- Fix: docs cd.
    
### Other

- Bump version: 0.4.0 → 0.4.1.
    
## v0.4.0 (2025-10-18)

### Fixes

- Fix: formatting.
    
### New

- Add API documentation for AskEndpoint.
    
  This commit adds API documentation for the `AskEndpoint` class and the new `QueryBuilder`.

  - A new `docs/api/ask_endpoint.md` file has been created with detailed explanations and examples for the `query` method and `QueryBuilder`.
  - A new `docs/README.md` file has been added to serve as a central hub for all documentation.
### Other

- Bump version: 0.3.0 → 0.4.0.
    
- Feat: Add automatic documentation with pdoc.
    
  This commit adds pdoc to the project to automatically generate API documentation.

  It also includes a new GitHub Action that builds the documentation and deploys it to GitHub Pages on every push to the main branch.

  The existing documentation has been moved to the `docs/pdoc` directory and is now included in the generated documentation. The `docs/README.md` has been updated to link to the new documentation.
## v0.3.0 (2025-10-18)

### Fixes

- Fix. formatting.
    
### Other

- Bump version: 0.2.6 → 0.3.0.
    
- Feat: Add query_dict method to AskEndpoint.
    
  Adds a new method `query_dict` to the `AskEndpoint` class to allow for the composition of complex Semantic MediaWiki queries using a structured dictionary.

  This new method supports conditions for categories, concepts, and properties with various operators, providing a more robust and programmatic way to build queries.

  Also includes:
  - A new `SMW_SYNTAX.md` file to document the syntax for the new method and provide examples for all existing query methods.
  - Comprehensive unit tests for the `query_dict` method to ensure its correctness and handle various input scenarios.
## v0.2.6 (2025-10-16)

### Fixes

- Fix broken documentation link in `pyproject.toml`.
    
  The documentation link on TestPyPI was returning a 404 error because it was using a placeholder username (`your-username`) instead of the correct one (`Kugeleis`).

  This commit updates the `[project.urls]` section in `pyproject.toml` to use the correct username, resolving the broken link.
### Other

- Bump version: 0.2.5 → 0.2.6.
    
## v0.2.5 (2025-10-16)

### Fixes

- Fix: Trigger publish workflow on tag push.
    
  The `publish-test.yml` workflow was previously configured to trigger on a GitHub release, which meant that pushing a tag did not automatically trigger the workflow.

  This change modifies the workflow to trigger on a tag push, which is the user's expected behavior.
### Other

- Bump version: 0.2.4 → 0.2.5.
    
- Uv tracks.
    
## v0.2.4 (2025-10-16)

### Fixes

- Fix: bump-my-version.
    
- Fix: version task.
    
### Other

- Bump version: 0.2.3 → 0.2.4.
    
- Chore: Refactor publish workflow.
    
- Feat: Add support for pre-releases and task for creating them.
    
## v0.2.2 (2025-10-16)

### Other

- Bump version: 0.2.1 → 0.2.2.
    
- Feat: add dev conainer.
    
## v0.2.1 (2025-10-15)

### New

- New venv.
    
- Add GitHub Actions workflow for Python package publishing.
    
  This workflow automates the process of uploading a Python package to PyPI when a release is created. It includes steps for building the package and publishing it securely.
### Other

- Bump version: 0.2.0 → 0.2.1.
    
## v0.2.0 (2025-10-15)

### New

- Add version-test.
    
  test package against python versions
### Other

- Bump version: 0.1.2 → 0.2.0.
    
## v0.1.2 (2025-10-15)

### Fixes

- Fix maintainer.
    
### Other

- Bump version: 0.1.1 → 0.1.2.
    
## v0.1.1 (2025-10-15)

### New

- Add boxmatrix example.
    
- Add testing and example usage.
    
- Add development tools.
    
### Other

- Bump version: 0.1.0 → 0.1.1.
    
- Drop examples.
    
- Better readme.
    
- Minimal examples added.
    
- Example working.
    
- A first step.
    
- Init.
    
### Updates

- Improve project setup.
    

