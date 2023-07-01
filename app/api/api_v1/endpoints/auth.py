# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     auth
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
from typing import Optional, Any

import httpx
from fastapi import APIRouter, status, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api import deps
from app.core.auth import authenticate, create_access_token
from app.schemas.user import UserCreate
from app.models.user import User

router = APIRouter()


@router.post('/signup',
             response_model=schemas.User,
             status_code=status.HTTP_201_CREATED)
def create_user_signup(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate
):
    """
    Create new user without the need to be logged in.
    :param db:
    :param user_in:
    :return:
    """
    user = db.query(User).filter(User.email == user_in.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password ")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged-in user.
    """

    user = current_user
    return user
