# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crud_user
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from typing import Optional
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.db import Session
from app.models import Recipe
from app.schemas import RecipeUpdate, RecipeCreate


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...



recipe = CRUDRecipe(Recipe)
