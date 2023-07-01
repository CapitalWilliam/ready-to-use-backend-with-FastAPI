# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     user
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

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False


class UserCreate(UserBase):
    email: EmailStr


class UserUpdate(UserBase):
    ...
