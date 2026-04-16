"""Logging helpers."""

import logging


def setup_logging() -> None:
    """Configure root logging once for the app."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


logger = logging.getLogger("merchant_ops_agent")
