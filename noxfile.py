"""Nox sessions."""

import nox
import tempfile

from nox.sessions import Session
from typing import Any

locations = "src", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "lint", "mypy", "pytype", "tests"

package = "iitp_6_python"


@nox.session(python=["3.8", "3.10"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    Args:
        session (Session): The session object.
        *args (str): Additional positional arguments representing package names.
        **kwargs (Any): Additional keyword arguments representing package options.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--requirement={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.10"])
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.8", "3.10"])
def tests(session: Session) -> None:
    """Run the test suite.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.8", "3.10"])
def lint(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages.

    Args:
        session (Session): The session object.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8", "3.10"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest.

    Args:
        session (Session): The session object.
    """
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation.

    Args:
        session (Session): The session object.
    """
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
