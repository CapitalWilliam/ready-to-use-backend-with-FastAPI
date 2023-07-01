# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     init_db
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

from sqlalchemy.orm import Session
from app import crud, schemas
from app import models
from recipe_data import RECIPES

logger = logging.getLogger(__name__)
FIRST_SUPERUSER = "admin@recipeapi.com"


# make sure all SQL Alchemy models are imported (models) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                firstname="Initial SuperUser",
                email=FIRST_SUPERUSER,
                is_superuser=True,

            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.recipes:
            for r in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=r["label"],
                    source=r["source"],
                    url=r["url"],
                    submitter_id=user.id
                )
                crud.recipe.create_with_submitter(db, obj_in=recipe_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"

        )
