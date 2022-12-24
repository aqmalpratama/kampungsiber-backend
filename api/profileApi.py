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

profile_api = Blueprint('profile_api', __name__)

@profile_api.route('/profile/user/<int:user_id>', methods=['GET'])
def userProfile(user_id):
    try:
        sql = "select * from user_profile where user_id = %s"
        data = (user_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        rows = cursor.fetchone()
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

@profile_api.route('/profile/mentor/<int:mentor_id>', methods=['GET'])
def mentorProfile(mentor_id):
    try:
        sql = "select * from user_profile where user_id = %s and reg_type = 1"
        data = (mentor_id)
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        rows = cursor.fetchone()
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

@profile_api.route('/profile/corporate/<int:id>', methods=['GET'])
def corporateProfile(id):
    try:
        if 'email' in session:
            sql = "select id, name, email, user_id from business_main where id = %s"
            data = (id)
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            rows = cursor.fetchone()
            if rows:
                response = jsonify(rows)
                response.status_code = 200
            else:
                response = jsonify({'message' : 'No profile'})
                response.status_code = 400
        else:
            response = jsonify({'message' : 'Unauthorized access'})
            response.status_code = 401
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@profile_api.route('/profile/individual/<int:id>', methods=['PUT'])
def updateIndividualProfile(id):
    try:
        data = request.form
        name = data['name']
        email = data['email']
        if 'email' in session:
            sql = "UPDATE `individual_main` SET `name`=%s, `email`=%s WHERE `id`=%s"
            data = (name, email, id)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify({'message' : 'Profile updated'})
            response.status_code = 200
        else:
            response = jsonify({'message' : 'Unauthorized access'})
            response.status_code = 401
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@profile_api.route('/profile/mentor/<int:user_id>', methods=['PUT'])
def updateMentorProfile(user_id):
    return jsonify({'message' : 'Profile updated'})

@profile_api.route('/profile/corporate/<int:user_id>', methods=['PUT'])
def updateCorporateProfile(user_id):
    return jsonify({'message' : 'Profile updated'})
