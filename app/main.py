# import out
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, APIRouter, status, Request, Depends, Query
from fastapi.exceptions import HTTPException

from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

# import in
from app import crud
from app.api import deps
from app.api.api_v1.api import api_router
from app.core import settings
from app.db import Session

from app.schemas.recipe import Recipe, RecipeSearchResults, RecipeCreate

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


@root_router.get("/", status_code=status.HTTP_200_OK)
def root(
        request: Request,
        db: Session = Depends(deps.get_db)
):
    recipes = crud.recipe.get_multi(db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes}
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug", reload=True)
