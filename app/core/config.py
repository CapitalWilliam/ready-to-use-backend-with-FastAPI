# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from typing import List, Union

from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):  # 1
    API_V1_STR: str = "/api/v1"  # 2

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)  # 3
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    FIRST_SUPERUSER = "admin@recipeapi.com"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1383@localhost/mydata'

    class Config:
        case_sensitive = True  # 4


settings = Settings()  # 5
