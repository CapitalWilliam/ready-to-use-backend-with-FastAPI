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

from typing import Optional

from fastapi import APIRouter, status, Request, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults

router = APIRouter()


@router.get('/recipe/{recipe_id}', status_code=status.HTTP_200_OK,
            response_model=Recipe)
async def fetch_recipe(*, recipe_id: str, db: Session = Depends(deps.get_db)):
    result = crud.recipe.get(db, recipe_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Recipe with ID {recipe_id} not found'
        )
    return result


@router.get('/search/',
            status_code=status.HTTP_200_OK,
            response_model=RecipeSearchResults)
async def search_recipes(*,
                         keyword: Optional[str] = Query(None, min_length=3, example='chicken'),
                         max_results: Optional[int] = 10,
                         db: Session = Depends(deps.get_db)):
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}
    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/recipe", status_code=status.HTTP_201_CREATED,
             response_model=Recipe)
async def create_recipe(
        *,
        recipe_in: RecipeCreate,
        db: Session = Depends(deps.get_db)
):
    return crud.recipe.create(db, obj_in=recipe_in)


