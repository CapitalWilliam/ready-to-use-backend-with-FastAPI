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

    def create_with_submitter(self, db: Session, obj_in: RecipeCreate) -> Optional[Recipe]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


recipe = CRUDRecipe(Recipe)
