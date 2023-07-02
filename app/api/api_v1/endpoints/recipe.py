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

import asyncio
from typing import Optional

import httpx
from fastapi import APIRouter, status,  Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults

router = APIRouter()


@router.get('/{recipe_id}', status_code=status.HTTP_200_OK,
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


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=Recipe)
async def create_recipe(
        *,
        recipe_in: RecipeCreate,
        db: Session = Depends(deps.get_db)
):
    return crud.recipe.create(db, obj_in=recipe_in)


async def get_reddit_top_async(subreddit: str, data: dict) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"},
        )

    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data


def get_reddit_top(subreddit: str, data: dict) -> None:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"},

    )
    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["chilren"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]

        subreddit_data.append(f"{str(score)}:{title}({link})")
    data[subreddit] = subreddit_data


@router.get("/ideas/async")
async def get_reddit_data_api_async():
    data = {}
    await asyncio.gather(
        get_reddit_top_async("recipes", data),
        get_reddit_top_async("easyrecipes", data),
        get_reddit_top_async("TopSecretRecipes", data)
    )
    return data


@router.get("/ideas/")
async def get_reddit_data_api():
    data = {}

    get_reddit_top("recipes", data)
    get_reddit_top("easyrecipes", data)
    get_reddit_top("TopSecretRecipes", data)

    return data
