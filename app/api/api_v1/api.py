# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     api
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from fastapi import APIRouter

from app.api.api_v1.endpoints import recipe

api_router = APIRouter()
api_router.include_router(recipe.router, prefix="/recipes", tags=["recipes"])
