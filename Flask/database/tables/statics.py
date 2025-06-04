import datetime
import sqlalchemy
from sqlalchemy import orm

from Flask.database.db_session import SqlAlchemyBase


class Statics(SqlAlchemyBase):
    __tablename__ = 'statics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    task1 = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    task2 = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    task3 = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f'Id: {self.id}; User_id: {self.user_id}; task1: {self.task1}; task2: {self.task2}; task3: {self.task3}'