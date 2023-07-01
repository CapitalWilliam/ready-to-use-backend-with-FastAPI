# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     deps.py
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

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core import settings
from app.core.auth import oauth2_scheme
from app.db import Session
from app.models import User


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db():
    db = Session()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
