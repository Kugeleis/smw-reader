# Changelog

## Unreleased (2025-10-20)

### Fixes

- Fix: align bump-my-version and generate-changelog configurations.
    
### Other

- Build: stop tracking uv.lock.
    
- Build: ignore uv.lock.
    
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
    
- Fix. formatting.
    
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

### Fixes

- Fix maintainer.
    
### New

- New venv.
    
- Add GitHub Actions workflow for Python package publishing.
    
  This workflow automates the process of uploading a Python package to PyPI when a release is created. It includes steps for building the package and publishing it securely.
- Add version-test.
    
  test package against python versions
- Add boxmatrix example.
    
- Add testing and example usage.
    
- Add development tools.
    
### Other

- Bump version: 0.2.1 → 0.2.2.
    
- Feat: add dev conainer.
    
- Bump version: 0.2.0 → 0.2.1.
    
- Bump version: 0.1.2 → 0.2.0.
    
- Bump version: 0.1.1 → 0.1.2.
    
- Bump version: 0.1.0 → 0.1.1.
    
- Drop examples.
    
- Better readme.
    
- Minimal examples added.
    
- Example working.
    
- A first step.
    
- Init.
    
### Updates

- Improve project setup.
    

