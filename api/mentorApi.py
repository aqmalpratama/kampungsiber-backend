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

mentor_api = Blueprint('mentor_api', __name__)

@mentor_api.route('/approve/mentor', methods=['GET'])
def getMentorApprove():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `user` WHERE `reg_type` = 1 and `is_acc_admin` = 1")
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
    
@mentor_api.route('/upcoming-consultation/mentor/<int:mentor_id>', methods=['GET'])
def getUpcomingConsultationMentor(mentor_id):
    try:
        sql = "select id, requestor_id, mentor_id, consultation_date, date_format(start_time, '%%T') as start_time, date_format(end_time, '%%T') as end_time, is_accepted_admin from consultation_request cr where cast(concat(consultation_date , ' ', start_time) as datetime) > now() and requestor_id = %s and is_accepted_admin = 1"
        data = (mentor_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        print(cursor._last_executed)
        rows = cursor.fetchall()
        if rows:
            response = jsonify(rows)
            response.status_code = 200
        else:
            response = jsonify({'message' : 'No upcoming consultation'})
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify( {'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response



