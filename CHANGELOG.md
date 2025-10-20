# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.6.13] - 2025-10-19

### Changed
- Refactored the `AskEndpoint` to simplify its interface, focusing on the `query` method and the `QueryBuilder`.
- Updated the `query_category` method to use the `QueryBuilder` internally.
- Aligned documentation and examples with the new `QueryBuilder`-focused approach.

### Removed
- Deprecated methods from `AskEndpoint`: `ask`, `query_pages`, `query_concept`, `query_property_value`, and `query_dict`.

### Fixed
- Updated the test suite to reflect the changes in `AskEndpoint`.

_Note: Changelog entries for versions 0.1.2 to 0.6.12 were not recorded. These versions included dependency updates and minor internal refactorings._

## [0.1.1] - 2025-10-15

### Added
- Initial release of SMW Reader
- Modular client architecture for Semantic MediaWiki APIs
- Ask endpoint with convenience methods for common queries
- Auto-formatted printouts (no manual "?" prefixes needed)
- Full backward compatibility with traditional SMW query syntax
- Comprehensive type hints throughout codebase
- Robust error handling with custom exceptions
- No external dependencies for basic HTTP functionality

### Features
- `query_category()` - Query pages by category with auto-formatting
- `query_property_value()` - Query by property-value pairs
- `query_concept()` - Query by SMW concepts
- `query_pages()` - Multi-condition queries with sorting
- `ask()` / `execute()` - Direct SMW query execution for advanced cases
- Automatic printout formatting while maintaining full backward compatibility

## [0.1.0] - 2025-10-15

### Added
- Initial development release
- Core SMW client functionality
- Ask endpoint implementation
- Comprehensive test suite (59 tests)
- Development tooling setup (ruff, mypy, pre-commit)
- Documentation and examples
