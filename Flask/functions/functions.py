import datetime
from random import randint, sample

from Flask.database.database import User, Tasks
from Flask.database.constants import TASKS

def get_days(user, date_only=False):
    date_now = datetime.datetime.now().date()
    if date_only:
        return date_now
    return (date_now - user.created_date.date()).days


def get_tasks(user, session):
    date_now = get_days(user, date_only=True).strftime("%Y-%m-%d")
    result = session.query(Tasks).filter((Tasks.user_id == user.id) & (Tasks.date == date_now)).first()
    if not result:
        generate_task(user, session)
        result = session.query(Tasks).filter((Tasks.user_id == user.id) & (Tasks.date == date_now)).first()

    return result


def generate_task(user: User, session):
    days = get_days(user)

    tasks = TASKS[days]
    res = {'day': tasks['day']}
    if user.swimming and randint(1, 5) < 3:
        res[3] = tasks['tasks'][-1]
    if user.bike and randint(1, 5) < 3:
        res[2] = tasks['tasks'][-2]

    num = 1
    if not res.get(2, 0):
        num += 1
    if not res.get(3, 0):
        num += 1

    other_tasks = sample(tasks['tasks'][:3], num)
    for task in other_tasks:
        if not res.get(1, 0):
            res[1] = task
        elif not res.get(2, 0):
            res[2] = task
        else:
            res[3] = task

    res_list = []
    for i in range(1, 4):
        task = res[i]
        res_list.append('__'.join([task['activity'], task['amount'], task['description']]))

    task = Tasks(user_id=user.id, text1=res_list[0], text2=res_list[1], text3=res_list[2])
    session.add(task)
    session.commit()
