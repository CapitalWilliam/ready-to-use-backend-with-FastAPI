# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     backen_pre_start
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

import logging

from sqlalchemy import text
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

from app.db import Session

logger = logging.getLogger(__name__)
max_tries = 60 * 5  # 5 minutes
wait_seconds = 1
import logging

logging.basicConfig(level=logging.INFO)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = Session()
        # Try to create session to check if DB is awake
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
