"""Independent daily attendance report. Safe to run from cron."""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.countdown_service import is_report_date_active
from revelacion_de_genero.services.email_service import already_sent, send_daily_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("daily-report")


def main() -> int:
    now = datetime.now(settings.timezone)
    day_key = now.date().isoformat()
    if not is_report_date_active(now):
        logger.info("Reporting window closed after %s. Nothing to send.", settings.report_end_date)
        return 0
    if already_sent(day_key):
        logger.info("Report for %s was already sent.", day_key)
        return 0
    result = send_daily_report(now=now)
    if result.get("sent"):
        logger.info("Report sent for %s.", day_key)
        return 0
    logger.error("Report was not sent for %s (%s).", day_key, result.get("error", "unknown"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
