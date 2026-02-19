"""
API package.

Houses all versioned API sub-packages.  Each version lives under its own
sub-package (e.g. :mod:`app.api.v1`) and exposes an :class:`~fastapi.APIRouter`
that is mounted in :mod:`app.main`.
"""
