# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     recipe
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from typing import Sequence

from pydantic import BaseModel, HttpUrl


class RecipeBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class RecipeCreate(RecipeBase):
    submitter_id: int


class RecipeUpdate(RecipeBase):
    label: str


class RecipeInDBBase(RecipeBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


class Recipe(RecipeInDBBase):
    pass


class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]
