from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import time

from app import flask_app

flask_app.secret_key = '123456789'

# flask_app.config['MYSQL_HOST'] = '127.0.0.1'
flask_app.config['MYSQL_HOST'] = 'host address'
flask_app.config['MYSQL_USER'] = 'user name'
flask_app.config['MYSQL_PASSWORD'] = 'user password'
flask_app.config['MYSQL_DB'] = 'database name'
flask_app.config['MYSQL_PORT'] = 'port number'

# Intialize MySQL
mysql = MySQL(flask_app)

@flask_app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['name'])
    return redirect(url_for('login'))

@flask_app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE user_id = %s', [session['user_id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@flask_app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    # username과 password에 입력값이 있을 경우
    if request.method == 'POST' and 'user_id' in request.form and 'password' in request.form:
        # 쉬운 checking을 위해 변수에 값 넣기
        user_id = request.form['user_id']
        password = request.form['password']
        # MySQL DB에 해당 계정 정보가 있는지 확인
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE user_id = %s AND password = %s', (user_id, password))
        # 값이 유무 확인 결과값 account 변수로 넣기
        account = cursor.fetchone()
        # 정상적으로 유저가 있으면 새로운 세션 만들고, 없으면 로그인 실패 문구 출력하며 index 리다이렉트
        if account:
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['name'] = account['name']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Creating User Page'
    if 'loggedin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST'\
            and 'user_id' in request.form\
            and 'password' in request.form\
            and 'name' in request.form\
            and 'email' in request.form:
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']

        # check user_id and email already exist
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE user_id = %s', [user_id])
        user_id_check = cursor.fetchone()

        cursor.execute('SELECT * FROM accounts WHERE email = %s', [email])
        email_check = cursor.fetchone()
        if user_id_check:
            msg = 'That user id is already exists!'
        elif email_check:
            msg = 'That email is already exists!'
        else:
            # new account creation
            sql_script = "INSERT INTO accounts (user_id, password, name, sign_up_date, email) VALUES (%s, %s, %s, %s, %s)"
            # cursor.execute(sql_script, [user_id, password, name, time.strftime('%Y-%m-%d'), email])
            cursor.execute(sql_script, [user_id, password, name, time.strftime('%Y-%m-%d %H:%M:%S'), email])
            mysql.connection.commit()
            msg = 'Create User Success!'
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

@flask_app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect(url_for('login'))