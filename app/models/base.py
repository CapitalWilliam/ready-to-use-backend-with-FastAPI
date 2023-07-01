# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     base
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from typing import Dict, Any

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr

class_registry: Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
