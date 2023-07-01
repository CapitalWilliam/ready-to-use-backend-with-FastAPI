# import out
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, APIRouter, status, Request, Depends,Query
from fastapi.exceptions import HTTPException

from fastapi.templating import Jinja2Templates

# import in
from app import crud
from app.db import Session
from app import deps

from app.schemas.recipe import Recipe,RecipeSearchResults,RecipeCreate

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
def root(
        request: Request,
        db: Session = Depends(deps.get_db)
):
    recipes = crud.recipe.get_multi(db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes}
    )


@api_router.get('/recipe/{recipe_id}', status_code=status.HTTP_200_OK,
                response_model=Recipe)
async def fetch_recipe(*, recipe_id: str, db: Session = Depends(deps.get_db)):
    result = crud.recipe.get(db, recipe_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Recipe with ID {recipe_id} not found'
        )
    return result


@api_router.get('/search/',
                status_code=status.HTTP_200_OK,
                response_model=RecipeSearchResults)
async def search_recipes(*,
                         keyword: Optional[str] = Query(None,min_length=3, example='chicken'),
                         max_results: Optional[int] = 10,
                         db: Session = Depends(deps.get_db)):
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}
    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}

@api_router.post("/recipe",status_code=status.HTTP_201_CREATED,
                 response_model=Recipe)
async def create_recipe(
        *,
        recipe_in:RecipeCreate,
        db:Session=Depends(deps.get_db)
):
    return crud.recipe.create(db,obj_in=recipe_in)


app.include_router(api_router)
