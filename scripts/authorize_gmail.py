"""Authorize Gmail locally without sending a message."""

from __future__ import annotations

import logging

from revelacion_de_genero.services.email_service import authorize_gmail

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main() -> int:
    try:
        authorize_gmail()
    except Exception as exc:
        logging.error("Gmail authorization failed (%s).", type(exc).__name__)
        return 1
    logging.info("Gmail authorization completed. No email was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
