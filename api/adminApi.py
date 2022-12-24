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

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/admin/waitinglist-mentor', methods=['GET'])
def waitinglistMentor():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, user_id, full_name, email, is_approved_admin, date_format(birth_date, '%Y-%m-%d') as birth_date, photo_name, no_phone, rate_per_hour FROM `user_profile` WHERE `is_approved_admin` is NULL and `reg_type` = 1")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@admin_api.route('/admin/approval-mentor', methods=['POST'])
def approval_mentor():
    try:
        data = request.form
        mentor_id = data['mentor_id']
        is_approved = int(data['is_approved'])
        if request.method == 'POST':
            sql = "update user_profile set is_approved_admin = %s where user_id = %s"
            data = (is_approved, mentor_id)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            
            sql = "select email from user where id = %s"
            data = (mentor_id)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            email = rows['email']
            connection.commit()
            if is_approved == 1:
                msg = Message(sender = 'aqmal.dev81@gmail.com', recipients = [email], subject = 'Approved Mentor', body = 'Berikut adalah lampiran perjanjian yang harus anda baca dan tanda tangani')
                msg.attach('Partnership Agreement draft.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', open('uploads/agreement/Partnership Agreement draft.docx', 'rb').read())
                mail.send(msg)
                response = jsonify({'message' : 'Mentor approved'})
                response.status_code = 200
            elif is_approved == 0:
                msg = Message(sender = 'aqmal.dev81@gmail.com', recipients = [email], subject = 'Reject Mentor', body = 'Maaf anda tidak dapat menjadi mentor di aplikasi ini')
                mail.send(msg)
                response = jsonify({'message' : 'Mentor rejected'})
                response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@admin_api.route('/admin/verify-payment', methods=['POST'])
def approval_consultation():
    try:
        data = request.form
        consultation_id = data['consultation_id']
        is_verify = int(data['is_verify'])
        zoom_link = data['zoom_link']
        if request.method == 'POST':

            if is_verify == 1:
                sql = "update consultation_request set verify_payment = %s, zoom_link = %s where id = %s"
                data = (is_verify, zoom_link, consultation_id)
                connection = mysql.connect()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql, data)
                connection.commit()
                response = jsonify({'message' : 'payment verified'})
                response.status_code = 200
            elif is_verify == 0:
                sql = "update consultation_request set verify_payment = %s, where id = %s"
                data = (is_verify, zoom_link, consultation_id)
                connection = mysql.connect()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql, data)
                connection.commit()
                response = jsonify({'message' : 'payment rejected'})
                response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response