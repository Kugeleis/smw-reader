"""Development tasks using duty.

Note: Some tools (mypy, bandit) are temporarily disabled in pre-commit
due to configuration issues but can still be run manually via duty tasks.
"""

from __future__ import annotations

import re
from pathlib import Path

from duty import duty


def get_supported_python_versions() -> list[str]:
    """Extract supported Python versions from pyproject.toml classifiers."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        # Fallback to default versions if pyproject.toml is not found
        return ["3.10", "3.11", "3.12", "3.13"]

    content = pyproject_path.read_text()
    # Match Python version classifiers like "Programming Language :: Python :: 3.10"
    pattern = r'"Programming Language :: Python :: (3\.\d+)"'
    matches = re.findall(pattern, content)

    # Filter out the generic "3" classifier and sort versions
    versions = [v for v in matches if "." in v]
    versions.sort(key=lambda x: tuple(map(int, x.split("."))))

    return versions if versions else ["3.10", "3.11", "3.12", "3.13"]


# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / "src"
TESTS_PATH = PROJECT_ROOT / "tests"
DOCS_PATH = PROJECT_ROOT / "docs"


@duty
def format(ctx) -> None:
    """Format code with ruff."""
    ctx.run("ruff format .", title="Formatting code")


@duty
def lint(ctx) -> None:
    """Run linting with ruff."""
    ctx.run("ruff check .", title="Linting code")


@duty
def lint_fix(ctx) -> None:
    """Run linting with ruff and fix issues automatically."""
    ctx.run("ruff check --fix .", title="Linting and fixing code")


@duty
def type_check(ctx) -> None:
    """Run type checking with mypy."""
    ctx.run("mypy src/", title="Type checking")


@duty
def test(ctx) -> None:
    """Run tests with pytest."""
    ctx.run("pytest", title="Running tests")


@duty
def test_cov(ctx) -> None:
    """Run tests with coverage."""
    ctx.run(
        "pytest --cov=src/smw_reader --cov-report=html --cov-report=term-missing",
        title="Running tests with coverage",
    )


@duty
def test_watch(ctx) -> None:
    """Run tests in watch mode."""
    ctx.run("pytest-watch", title="Running tests in watch mode")


@duty
def test_versions(ctx) -> None:
    """Test package across Python versions with uv."""
    versions = get_supported_python_versions()

    if not versions:
        print("❌ No Python versions found in pyproject.toml")
        return

    print(f"Found supported Python versions: {', '.join(versions)}")

    for version in versions:
        print(f"Testing Python {version}...")
        ctx.run(
            f"uv run --python {version} --with . python -c 'import smw_reader; print(\"✅ Success\")'",
            title=f"Testing Python {version}",
        )


@duty
def security(ctx) -> None:
    """Run security checks with bandit."""
    ctx.run("bandit -r src/", title="Running security checks")


@duty
def deps_check(ctx) -> None:
    """Check for dependency vulnerabilities."""
    ctx.run("pip-audit", title="Checking dependencies for vulnerabilities")


@duty
def clean(ctx) -> None:
    """Clean up build artifacts and cache files."""
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        "dist",
        "build",
        "*.egg-info",
        ".mypy_cache",
        ".ruff_cache",
    ]

    for pattern in patterns:
        ctx.run(
            f"find . -name '{pattern}' -type d -exec rm -rf {{}} + 2>/dev/null || true",
            title=f"Cleaning {pattern}",
        )
        ctx.run(
            f"find . -name '{pattern}' -type f -delete 2>/dev/null || true",
            title=f"Cleaning {pattern}",
        )


@duty
def install(ctx) -> None:
    """Install the project in development mode."""
    ctx.run("uv sync", title="Installing dependencies")


@duty
def install_dev(ctx) -> None:
    """Install development dependencies."""
    ctx.run("uv sync --all-extras", title="Installing all dependencies")


@duty
def build(ctx) -> None:
    """Build the package."""
    ctx.run("uv build", title="Building package")


@duty
def check_all(ctx) -> None:
    """Run all checks (format, lint, type-check, test)."""
    format(ctx)
    lint(ctx)
    type_check(ctx)
    test(ctx)


@duty
def pre_commit(ctx) -> None:
    """Run pre-commit checks."""
    ctx.run("pre-commit run --all-files", title="Running pre-commit hooks")


@duty
def pre_commit_install(ctx) -> None:
    """Install pre-commit hooks."""
    ctx.run("pre-commit install", title="Installing pre-commit hooks")


@duty
def docs_build(ctx) -> None:
    """Build documentation."""
    if DOCS_PATH.exists():
        ctx.run("sphinx-build docs docs/_build", title="Building documentation")
    else:
        print("No docs directory found. Skipping documentation build.")


@duty
def docs_serve(ctx) -> None:
    """Serve documentation locally."""
    if DOCS_PATH.exists():
        ctx.run("sphinx-autobuild docs docs/_build", title="Serving documentation")
    else:
        print("No docs directory found. Skipping documentation serving.")


@duty
def update_deps(ctx) -> None:
    """Update dependencies."""
    ctx.run("uv lock --upgrade", title="Updating dependencies")


@duty
def example(ctx) -> None:
    """Run the example script."""
    ctx.run("python example.py", title="Running example script")


@duty
def profile(ctx) -> None:
    """Profile the code."""
    ctx.run("python -m cProfile -o profile.stats example.py", title="Profiling code")
    cmd = 'python -c "import pstats; pstats.Stats(\\"profile.stats\\").sort_stats(\\"cumulative\\") \
        .print_stats(20)"'
    ctx.run(cmd, title="Showing profile stats")


@duty
def benchmark(ctx) -> None:
    """Run benchmarks if available."""
    benchmark_files = list(TESTS_PATH.glob("**/bench_*.py"))
    if benchmark_files:
        ctx.run("pytest -v -k bench", title="Running benchmarks")
    else:
        print("No benchmark files found (bench_*.py in tests/).")


@duty
def init_project(ctx) -> None:
    """Initialize project with pre-commit hooks and dev dependencies."""
    install_dev(ctx)
    if (PROJECT_ROOT / ".pre-commit-config.yaml").exists():
        pre_commit_install(ctx)
    print("Project initialized successfully!")
