"""Test across supported Python versions; versions come from pyproject.toml classifiers."""

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_venv = "yes"  # `uv sync --locked` still runs; force fresh with --reuse-venv=no

PYTHON_VERSIONS = nox.project.python_versions(nox.project.load_toml("pyproject.toml"))


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run `make test` in an env synced from uv.lock; posargs are not forwarded."""
    # UV_PROJECT_ENVIRONMENT on both calls; without it `uv run` uses the project .venv
    env = {"UV_PROJECT_ENVIRONMENT": session.virtualenv.location}
    session.run_install(
        "uv", "sync", "--locked", f"--python={session.virtualenv.location}", env=env
    )
    session.run("make", "test", env=env, external=True)
