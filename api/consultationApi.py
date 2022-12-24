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

consultation_api = Blueprint('consultation_api', __name__)

@consultation_api.route('/consultation/mentor-approve', methods=['GET'])
def consultationMentor():
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

@consultation_api.route('/consultation', methods=['POST'])
def createConsultationSession():
    try:
        data = request.form
        requestorId = data['requestor_id']
        mentorId = data['mentor_id']
        consultationDate = data['consultation_date']
        availTimeId = data['avail_time_id']

        sql = "INSERT INTO `consultation_request` (`requestor_id`, `mentor_id`, `consultation_date`, `avail_time_id`) VALUES (%s,%s,%s,%s)"
        data = (requestorId, mentorId, consultationDate, availTimeId)
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        response = jsonify({'message' : 'Consultation session created'})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response
