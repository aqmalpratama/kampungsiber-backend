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

testimonial_api = Blueprint('testimonial_api', __name__)

@testimonial_api.route('/testimonial/compro', methods=['GET'])
def getTestimonialCompro():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `vw_testimonial_compro`")
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
    
@testimonial_api.route('/testimonial/mentor/<int:mentor_id>', methods=['GET'])
def getTestimonialMentor(mentor_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `vw_testimonial_mentor` WHERE mentor_id = %s", mentor_id)
        rows = cursor.fetchall()
        print(cursor._last_executed)
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
    
@testimonial_api.route('/testimonial/compro', methods=['POST'])
def createTestimonialCompro():
    try:
        data = request.form
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO `testimonial_compro` (`user_id`, `testimonial_content`, `created_date`) VALUES (%s, %s, %s)", (data['user_id'], data['testimonial_content'], data['created_date']))
        connection.commit()
        cursor.close()
        connection.close()
        response = jsonify({'message' : 'Testimonial created'})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response
    
@testimonial_api.route('/testimonial/mentor', methods=['POST'])
def createTestimonialMentor():
    try:
        data = request.form
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO `testimonial_mentor` (`requestor_id`, `mentor_id`, `testimonial_content`, `created_date`) VALUES (%s, %s, %s, %s)", (data['requestor_id'], data['mentor_id'], data['testimonial_content'], data['created_date']))
        connection.commit()
        cursor.close()
        connection.close()
        response = jsonify({'message' : 'Testimonial created'})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

