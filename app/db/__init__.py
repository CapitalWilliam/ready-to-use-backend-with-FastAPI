# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       Capital_Wu
   date：          2023/7/1
-------------------------------------------------
   Change Activity:
                   2023/7/1:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User

engine = create_engine('postgresql://postgres:1383@localhost/mydata')
Session = sessionmaker(bind=engine)
session = Session()

user = User(name='John', email='john@example.com')
session.add(user)
session.commit()
# 查询数据
users = session.query(User).all()
for user in users:
    print(user.name)