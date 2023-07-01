# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     initial_data
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

from app.db.init_db import init_db
from app.db import Session

# 在这个代码中运行init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    db = Session()
    init_db(db)


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial created")


if __name__ == '__main__':
    main()
