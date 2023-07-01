# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crud_user
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

from app.crud.base import CRUDBase
from app.db import Session
from app.models import User
from app.schemas import UserUpdate, UserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


user = CRUDUser(User)
