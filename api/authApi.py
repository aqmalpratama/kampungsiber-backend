import datetime
import pymysql
import os
import random

from flask_mail import Message
from flask import request, jsonify, session, render_template, redirect, url_for, Blueprint, render_template, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import app
from config import mysql, mail

auth_api = Blueprint('auth_api', __name__)

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
                    cursor.close()
                    connection.close()
                    response = jsonify({'message' : 'You are logged in'})
                    response.status_code = 200
                else:
                    response = jsonify({'message' : 'Invalid password'})
                    response.status_code = 400
            else:
                response = jsonify({'message' : 'Invalid email'})
                response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
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

            photo = upload_file(request.files.getlist('photo[]'), 'photo')
            
            sql = "INSERT INTO `user_profile` (`full_name`, `email`, `first_name`, `last_name`, `birth_date`, `university`, `no_phone`,`user_id`, `photo_name`, `reg_type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (full_name, email, first_name, last_name, birth_date, university, no_phone, user_id, photo, regType)
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
        cursor.execute("SELECT id, date_format(start_time, '%T') as start_time, date_format(end_time, '%T') as end_time FROM `available_consult_time`")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        return response

app.config['PHOTO_FOLDER'] = 'uploads/photo'
app.config['IJAZAH_FOLDER'] = 'uploads/ijazah'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg','jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(filenya, type):
    files = filenya
    errors = {}
    success = False
    filename = ''
    for file in files:      
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if type == 'photo':
                    file.save(os.path.join(app.config['PHOTO_FOLDER'], filename))
                elif type == 'ijazah':
                    file.save(os.path.join(app.config['IJAZAH_FOLDER'], filename))
                print('filename', filename)
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'
        else:
            filename = None
            success = True

    if success:
        response = filename
        # response.status_code = 201
        return response
    
    if errors:
        response = errors[file.filename]
        # response.status_code = 400
        return response
    