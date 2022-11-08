import os
import datetime
import requests


def create_user_tasks():
    try:
        tasks = get_tasks_by_user_id(user["id"], todos_json_list)
    except KeyError:
        return

    now_time = datetime.datetime.now()
    filename = f'tasks/{user["username"]}.txt'

    if os.path.exists(filename):
        file = open(filename)
        s = file.read()
        file_creation_time = ''
        index = 0
        for char in s:
            if char != '>':
                index += 1
            else:
                index += 2
                file_creation_time = f'{s[index+6:index+10]}-' \
                                     f'{s[index+3:index+5]}-' \
                                     f'{s[index:index+2]}-' \
                                     f'{s[index+11:index+13]}-' \
                                     f'{s[index+14:index+16]}'

        file.close()
        os.rename(filename, f'tasks/old_{user["username"]}-{file_creation_time}.txt')

    completed_tasks = ''
    failed_tasks = ''
    completed_counter = 0
    failed_counter = 0
    for task in tasks[0]:
        task = '- '+task
        if len(task) > 46:
            task = task[0:46] + '...'
        completed_tasks += task + '\n'
        completed_counter += 1

    for task in tasks[1]:
        task = '- ' + task
        if len(task) > 46:
            task = task[0:46] + '...'
        failed_tasks += task + '\n'
        failed_counter += 1

    if completed_tasks == '':
        completed_tasks = 'Нет завершённых задач'
    if failed_tasks == '':
        failed_tasks = 'Нет актуальных задач'
    counter = failed_counter+completed_counter

    with open(filename, 'w') as file:
        file.write(f'''# Отчёт для {user["company"]["name"]}
{user["name"]} <{user["email"]}> {now_time.strftime("%d.%m.%Y %H:%M")}\n
Всего задач: {counter}\n
## Актуальные задачи ({failed_counter}):
{failed_tasks}
## Завершённые задачи ({completed_counter}):
{completed_tasks}''')


def get_tasks_by_user_id(id, todos):
    completed_tasks = []
    failed_tasks = []
    try:
        for task in todos:
            if task["userId"] == id:
                if task['completed']:
                    completed_tasks.append(task['title'])
                else:
                    failed_tasks.append(task['title'])
    except KeyError:
        pass
    return completed_tasks, failed_tasks


request_users = requests.get('https://json.medrocket.ru/users')
request_todos = requests.get('https://json.medrocket.ru/todos')

users_json_list = request_users.json()
todos_json_list = request_todos.json()

try:
    os.mkdir('tasks')
except FileExistsError:
    pass

for user in users_json_list:
    create_user_tasks()
