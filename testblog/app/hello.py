# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request, url_for, session, g, redirect
from flask_redis import FlaskRedis

app = Flask(__name__)
bootstrap = Bootstrap()
bootstrap.init_app(app)
DEBUG = True

SECRET_KEY = 'Ice'
app.secret_key = SECRET_KEY

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'GET':
        return render_template('register.html', error=error)

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    position= request.form.get('position')

    user_id = str(g.db.incrby('next_user_id', 1000))
    g.db.hmset('user:'+user_id, dict(
        username=username, password=password, email=email,
        position=position
    ))
    g.db.hset('users', username, user_id)
    session['username'] = username
    if position == 'manager':
        return redirect(url_for('manager'))
    else:
        return redirect(url_for('tasks'))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error=error)
    username = request.form['username']
    password = request.form['password']
    user_id = str(g.db.hget('users', username), 'utf-8')
    if not user_id:
        error = 'No such user'
        return render_template('login.html', error=error)

    saved_password = str(g.db.hget('user:' + str(user_id), 'password'), 'utf-8')
    if password != saved_password:
        error = 'Incorrect password'
        return render_template('login.html', error=error)
    session['username'] = username
    user_position = str(g.db.hget('user:' + str(user_id), 'position'), 'utf-8')
    print(user_position)
    if user_position == 'manager':
        return redirect(url_for('manager'))
    else:
        init_employee(user_id)
        return redirect(url_for('tasks'))

def init_db():
    db = FlaskRedis(host='localhost', port='6378', db='0')
    db.init_app(app)
    return db

def init_employee(user_id)

@app.before_request
def before_request():
    g.db = init_db()

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if not session:
        return redirect(url_for('login'))
    user_id = g.db.hget('users', session['username'])
    print('userid:', user_id)
    if request.method == 'GET':
        return render_template('manager.html', timeline=_get_timeline(user_id))

    taskname = request.form['taskname']
    limittime= request.form['limittime']
    payback  = request.form['payback']

    task_id = str(g.db.incr('next_task_id'))
    g.db.hmset('task:' + task_id, dict(user_id=user_id,
                                       time=str(datetime.utcnow()),
                                       taskname=taskname,
                                       limittime=limittime,
                                       payback=payback))
    g.db.lpush('tasklit', str(task_id))
    g.db.lpush('tasks:' + str(user_id), str(task_id))
    g.db.lpush('timeline:' + str(user_id), str(task_id))
    g.db.ltrim('timeline:' + str(user_id), 0, 100)
    print('endpush')
    return render_template('manager.html', timeline=_get_timeline(user_id))

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if not session:
        return redirect(url_for('login'))
    user_id = g.db.hget('users', session['username'])
    tasklist = _tasklist()
    print(tasklist)
    if request.method == 'GET':
        print('startGET')
        return render_template('tasks.html', tasks=tasklist)

    taskid = request.form['taskid']
    prefer = request.form['prefer']
    g.db.hmset('task' + str(taskid) + '_prefer:',
               dict(user_id=user_id, prefer=prefer))

    return render_template('tasks.html', tasks=_tasklist())

def _get_timeline(user_id):
    tasks = g.db.lrange('timeline:' + str(user_id), 0, -1)
    timeline = []
    for task_id in tasks:
        task = g.db.hgetall('task:' + str(task_id, 'utf-8'))
        timeline.append(dict(
            username=g.db.hget('user:' + str(task[b'user_id'],
                                             'utf-8')+"000", 'username'),
            time=task[b'time'],
            taskname=task[b'taskname']))
    return timeline

def _tasklist():
    tasklist = g.db.lrange('tasklist', 0, -1)
    print('tasklist', tasklist)
    tasks = []
    for task_id in tasklist:
        task = g.db.hgetall('task:' + str(task_id, 'utf-8'))
        tasks.append(dict(
            taskid=str(task_id)[2:-1],
            name=str(task[b'taskname'])[2:-1],
            limittime=str(task[b'limittime'])[2:-1],
            payback=str(task[b'payback'])[2:-1]
        ))
    return tasks


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
