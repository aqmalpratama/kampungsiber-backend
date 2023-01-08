import pymysql
import os
import jwt
import uuid
import numpy as np

from flask_mail import Message
from flask import request, jsonify, session, render_template, redirect, url_for, Blueprint, render_template, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
from ast import literal_eval

from app import app
from config import mysql, mail

app.config['PHOTO_FOLDER'] = 'uploads/photo'
app.config['IJAZAH_FOLDER'] = 'uploads/ijazah'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'kampungsiber-key-dev'

auth_api = Blueprint('auth_api', __name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg','jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(filenya, type):
    files = filenya
    errors = {}
    success = False
    filename = ''
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + filename
            if type == 'photo':
                file.save(os.path.join(app.config['PHOTO_FOLDER'], filename))
            elif type == 'ijazah':
                file.save(os.path.join(app.config['IJAZAH_FOLDER'], filename))
            print('filename', filename)
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success:
        response = filename
        # response.status_code = 201
        return response
    
    if errors:
        response = errors[file.filename]
        # response.status_code = 400
        return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            sql = "SELECT * FROM `user` WHERE `id`=%s"
            where = (data['user_id'])
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, where) 
            print(cursor._last_executed)
            current_user = cursor.fetchone()
            print('current_user', current_user)
        except:
            return jsonify({'message' : 'Token is invalid !!'}), 401
        
        return f(current_user, *args, **kwargs)
  
    return decorated

@auth_api.route('/user', methods=['GET'])
@token_required
def get_user_login(current_user):
    try:
        sql = "SELECT * FROM `user_profile` WHERE `user_id`=%s"
        where = (current_user['id'])
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, where)
        rows = cursor.fetchone()
        if rows:
            response = jsonify({'message' : 'User found', 'status_code' : 200, 'data' : rows})
            # response.status_code = 200
        else:
            response = jsonify({'message' : 'User not found', 'status_code' : 400})
            # response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin', 'status_code' : 400})
        # response.status_code = 400
    finally:
        cursor.close()
        connection.close()
        return response

@auth_api.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.form
        email = data['email']
        password = data['password']
        if email and password and request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            checkPassword = rows['password']
            if rows:
                if check_password_hash(checkPassword, password):
                    session['email'] = email
                    session['userdata'] = rows
                    token = jwt.encode({'user_id' : rows['id'], 'exp' : datetime.utcnow() + timedelta(minutes=60)}, app.config['SECRET_KEY'])
                    cursor.close()
                    connection.close()
                    response = jsonify({'message' : 'You are logged in', 'status_code' : 200, 'token' : token})
                    # response.status_code = 200
                else:
                    response = jsonify({'message' : 'Invalid password', 'status_code' : 400})
                    # response.status_code = 400
            else:
                response = jsonify({'message' : 'Invalid email', 'status_code' : 400})
                # response.status_code = 400
        else:
            response = jsonify({'message' : 'Please fill out the form', 'status_code' : 400})
            # response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin', 'status_code' : 400})
        # response.status_code = 400
    finally:
        return response

@auth_api.route('/signout')
def signout():
    if 'email' in session:
        session.pop('email', None)
        response = jsonify({'message' : 'You have successfully logged out'})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message' : 'Unauthorized'})
        response.status_code = 401
        return response

@auth_api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form
        first_name = data['first_name']
        last_name = data['last_name']
        full_name = first_name + ' ' + last_name
        email = data['email']
        password = data['password']
        regType = int(data['reg_type'])
        linkedin = data['linkedin']
        birth_date = data['birth_date']
        university = data['university']
        no_phone = data['no_phone']
        avail_time = data['avail_time']
        tech_stack = data['tech_stack']
        rate_per_hour = data['rate_per_hour']
        
        if request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()

            if rows:
                response = jsonify({'message' : 'Email already exists'})
                response.status_code = 400
                return response

            sql = "INSERT INTO `user` (`email`,`password`,`reg_type`,`full_name`, `first_name`, `last_name`) VALUES (%s,%s,%s,%s,%s,%s)"
            data = (email, generate_password_hash(password), regType, full_name, first_name, last_name)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            user_id = cursor.lastrowid

            photo = None
            if 'photo[]' in request.files:
                photo = upload_file(request.files.getlist('photo[]'), 'photo')
                
            if rate_per_hour == '' or rate_per_hour is None:
                rate_per_hour = 0
            else:
                rate_per_hour = int(rate_per_hour)
                
            sql = "INSERT INTO `user_profile` (`full_name`, `email`, `first_name`, `last_name`, `birth_date`, `university`, `no_phone`,`user_id`, `photo_name`, `reg_type`, `linkedin`, `rate_per_hour`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (full_name, email, first_name, last_name, birth_date, university, no_phone, user_id, photo, regType, linkedin, rate_per_hour)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            
            check_time = avail_time is not None and avail_time != ''
            check_stack = tech_stack is not None and tech_stack != ''
            if regType == 1 and check_time and check_stack:
                avail_time = avail_time.split(',')
                for time in avail_time:
                    sql = "INSERT INTO `mentor_avail_time` (`mentor_id`, `avail_time_id`) VALUES (%s,%s)"
                    data = (user_id, time)
                    cursor = connection.cursor()
                    cursor.execute(sql, data)
                    
                sql = "INSERT INTO `mentor_stack` (`mentor_id`, `tech_id`) VALUES (%s,%s)"
                data = (user_id, tech_stack)
                cursor = connection.cursor()
                cursor.execute(sql, data)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({'message' : 'User created successfully'})
            response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@auth_api.route('/reset-password', methods=['POST'])
def resetPassword():
    try:
        data = request.form
        email = data['email']
        new_password = data['new_password']
        if email and new_password and request.method == 'POST':
            sql = "SELECT * FROM `user` WHERE `email`=%s"
            data = (email)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            if rows:
                sql = "UPDATE `user` SET `password`=%s WHERE `email`=%s"
                data = (generate_password_hash(new_password), email)
                cursor.execute(sql, data)
                connection.commit()
                cursor.close()
                connection.close()
                response = jsonify({'message' : 'Password changed'})
                response.status_code = 200
            else:
                response = jsonify({'message' : 'Invalid email'})
                response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@auth_api.route('/tech-stack', methods=['GET'])
def techStack():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `tech_stack`")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        return response
    
@auth_api.route('/avail-consult-time', methods=['GET'])
def availConsultTime():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, date_format(start_time, '%H:%i') as start_time, date_format(end_time, '%H:%i') as end_time FROM `available_consult_time` order by start_time asc")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        return response