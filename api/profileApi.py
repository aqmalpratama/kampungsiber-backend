import datetime
import pymysql
import os
import random

from flask_mail import Message
from flask import request, jsonify, session, render_template, redirect, url_for, Blueprint, render_template, abort, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import app
from config import mysql, mail

profile_api = Blueprint('profile_api', __name__)

@profile_api.route('/profile/<int:user_id>', methods=['GET'])
def userProfile(user_id):
    try:
        sql = "select * from user_profile left join `vw_mentor_stack` on `vw_mentor_stack`.`mentor_id` = `user_profile`.`user_id` where user_id = %s"
        data = (user_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        rows = cursor.fetchone()
        
        if rows['photo_name'] != None:
            root = os.path.dirname(os.path.abspath(__file__))
            photo_link = os.path.join(root, 'uploads', 'photo', rows['photo_name'])
            rows['photo_link'] = photo_link
            
        if rows:
            response = jsonify(rows)
            response.status_code = 200
        else:
            response = jsonify({'message' : 'No profile'})
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@profile_api.route('/profile/photo/<int:user_id>', methods=['GET'])
def userProfilePhoto(user_id):
    try:
        sql = "select photo_name from user_profile where user_id = %s"
        data = (user_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        rows = cursor.fetchone()
        if rows:
            return send_from_directory('uploads/photo', rows['photo_name'])
        else:
            abort(404)
    except Exception as e:
        print(e)
        abort(404)

@profile_api.route('/profile/<int:user_id>', methods=['POST'])
def updateUserProfile(user_id):
    try:
        data = request.form
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        print(data)
        cursor.execute("UPDATE `user_profile` SET `first_name` = %s, `last_name` = %s, `no_phone` = %s, `birth_date` = %s, `university` = %s, `title` = %s, `linkedin` = %s, `experience` = %s, `rate_per_hour` = %s, `email` = %s WHERE `user_id` = %s", (data['first_name'], data['last_name'], data['no_phone'], data['birth_date'], data['university'], data['title'], data['linkedin'], data['experience'], data['rate_per_hour'], data['email'], data['user_id']))
        print(cursor._last_executed)
        connection.commit()
        response = jsonify({'message' : 'Profile updated'})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response


@profile_api.route('/profile/avail-time/<int:user_id>', methods=['GET'])
def getUserAvailTime(user_id):
    try:
        sql = "select * from mentor_avail_time where mentor_id = %s"
        data = (user_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        rows = cursor.fetchall()
        if rows:
            response = jsonify(rows)
            response.status_code = 200
        else:
            response = jsonify({'message' : 'No profile'})
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

# @profile_api.route('/profile/mentor/<int:mentor_id>', methods=['GET'])
# def mentorProfile(mentor_id):
#     try:
#         sql = "select * from user_profile where user_id = %s and reg_type = 1"
#         data = (mentor_id)
#         connection = mysql.connect()
#         cursor = connection.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(sql, data)
#         rows = cursor.fetchone()
#         if rows:
#             response = jsonify(rows)
#             response.status_code = 200
#         else:
#             response = jsonify({'message' : 'No profile'})
#             response.status_code = 400
#     except Exception as e:
#         print(e)
#         response = jsonify({'message' : 'Something went wrong, contact admin'})
#         response.status_code = 400
#     finally:
#         return response

# @profile_api.route('/profile/corporate/<int:id>', methods=['GET'])
# def corporateProfile(id):
#     try:
#         if 'email' in session:
#             sql = "select id, name, email, user_id from business_main where id = %s"
#             data = (id)
#             connection = mysql.connect()
#             cursor = connection.cursor(pymysql.cursors.DictCursor)
#             cursor.execute(sql, data)
#             rows = cursor.fetchone()
#             if rows:
#                 response = jsonify(rows)
#                 response.status_code = 200
#             else:
#                 response = jsonify({'message' : 'No profile'})
#                 response.status_code = 400
#         else:
#             response = jsonify({'message' : 'Unauthorized access'})
#             response.status_code = 401
#     except Exception as e:
#         print(e)
#         response = jsonify({'message' : 'Something went wrong, contact admin'})
#         response.status_code = 400
#     finally:
#         return response

# @profile_api.route('/profile/individual/<int:id>', methods=['PUT'])
# def updateIndividualProfile(id):
#     try:
#         data = request.form
#         name = data['name']
#         email = data['email']
#         if 'email' in session:
#             sql = "UPDATE `individual_main` SET `name`=%s, `email`=%s WHERE `id`=%s"
#             data = (name, email, id)
#             connection = mysql.connect()
#             cursor = connection.cursor()
#             cursor.execute(sql, data)
#             connection.commit()
#             cursor.close()
#             connection.close()
#             response = jsonify({'message' : 'Profile updated'})
#             response.status_code = 200
#         else:
#             response = jsonify({'message' : 'Unauthorized access'})
#             response.status_code = 401
#     except Exception as e:
#         print(e)
#         response = jsonify({'message' : 'Something went wrong, contact admin'})
#         response.status_code = 400
#     finally:
#         return response

# @profile_api.route('/profile/mentor/<int:user_id>', methods=['PUT'])
# def updateMentorProfile(user_id):
#     return jsonify({'message' : 'Profile updated'})

# @profile_api.route('/profile/corporate/<int:user_id>', methods=['PUT'])
# def updateCorporateProfile(user_id):
#     return jsonify({'message' : 'Profile updated'})
