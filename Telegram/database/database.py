from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_login import UserMixin

engine = create_engine('sqlite:///Telegram/data/users_info.db')
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    flask = Column(Integer, nullable=True)
    logged = Column(Boolean, default=False)

    def __repr__(self):
        return f'Id: {self.id}; Flask_id: {self.flask}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
