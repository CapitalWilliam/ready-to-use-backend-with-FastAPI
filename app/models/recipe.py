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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    submitter = relationship('User', back_populates='recipes')
