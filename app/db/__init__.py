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
from app.core import settings

# todo
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()
if __name__ == '__main__':

    user = User(first_name='John Shit', email='john@example.com')
    users = session.query(User).all()
    session.add(user)
    session.commit()
    # 查询数据
    for user in users:
        print(user.first_name)
