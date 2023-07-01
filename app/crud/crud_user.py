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

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.db import Session
from app.models import User
from app.schemas import UserUpdate, UserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def is_exist(self, db: Session, *, email: str):
        if self.get_by_email(db, email):
            return True
        else:
            return False

    def create(self,
               db,
               obj_in):
        create_data = obj_in.dict()
        create_data.pop('password')
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()
        return db_obj

user = CRUDUser(User)
