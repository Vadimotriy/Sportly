import datetime
import sqlalchemy
from sqlalchemy import orm

from Flask.database.db_session import SqlAlchemyBase


class Statics(SqlAlchemyBase):
    __tablename__ = 'statics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    num1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    num2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date3 = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    bool4 = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')