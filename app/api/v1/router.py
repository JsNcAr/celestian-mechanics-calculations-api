"""DEPRECATED shim — renamed to :mod:`app.api.v1.routes`.

This module remains only to preserve backward-compatible imports for a
short transition period. Import the aggregator from
``app.api.v1.routes`` instead.
"""

import warnings

warnings.warn(
    "app.api.v1.router was renamed to app.api.v1.routes -- import from the new module",
    DeprecationWarning,
)

from app.api.v1.routes import router  # re-export for compatibility
