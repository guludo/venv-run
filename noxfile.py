"""nox config for venv-run."""

import nox


@nox.session(
    python=[f"{py}3.{x}" for py in ("", "pypy") for x in range(7, 13)] + ["pyston3"]
)
def test(session: nox.Session) -> None:
    """Run tests."""
    session.run(*"python -X dev -bb -m unittest discover".split() + session.posargs)
