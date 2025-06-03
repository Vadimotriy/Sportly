from Flask.database import db_session
from Flask.database.tables.users import User
from Flask.database.tables.statics import Statics

db_session.global_init("Flask/data/test.db")

if __name__ == '__main__':
    db_sess = db_session.create_session()

    news = Statics(task1=True, task3=True, user_id=1)
    db_sess.add(news)
    db_sess.commit()

    for user in db_sess.query(User).all():
        print(user.statics)

