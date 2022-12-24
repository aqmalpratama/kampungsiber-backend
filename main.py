import datetime
import urllib.request
import pymysql
import json

from flask import request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from config import mysql, mail
from api.authApi import auth_api
from api.mentorApi import mentor_api
from api.testimonialApi import testimonial_api
from api.profileApi import profile_api
from api.consultationApi import consultation_api
from api.adminApi import admin_api

app.register_blueprint(auth_api)
app.register_blueprint(mentor_api)
app.register_blueprint(testimonial_api)
app.register_blueprint(profile_api)
app.register_blueprint(consultation_api)
app.register_blueprint(admin_api)

@app.route('/mentor_stack')
def mentor_stack():
    sql = "select * from mentor_main join mentor_stack on mentor_main.id = mentor_stack.mentor_id join tech_stack on mentor_stack.tech _id = tech_stack.id"
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)

# dashboard
@app.route('/dashboard')
def dashboard():
    if 'userdata' in session:
        print(session)
        return render_template('dashboard.html', userdata=session['userdata'])
    else:
        return redirect(url_for('signin'))

@app.route('/dashboard/upcomingConsultation/<int:user_id>', methods=['GET'])
def upcomingConsultation(user_id):
    try:
        if 'email' in session:
            sql = "select id, requestor_id, mentor_id, consultation_date, date_format(start_time, '%%T') as start_time, date_format(end_time, '%%T') as end_time, is_accepted_mentor, payment_status from consultation_request cr where cast(concat(consultation_date , ' ', start_time) as datetime) > now() and requestor_id = %s and is_accepted_mentor = 1 and payment_status = 1"
            data = (user_id)
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
        else:
            response = jsonify({'message' : 'Unauthorized access'})
            response.status_code = 401
    except Exception as e:
        print(e)
        response = jsonify( {'message' : 'Something went wrong, contact admin'})
        response.status_code = 400
    finally:
        return response

@app.route('/dashboard/changeConsultationStatus/<int:user_id>', methods=['PUT'])
def changeConsultationStatus(user_id):
    try:
        data = request.form
        is_accepted_mentor = data['is_accepted_mentor']
        if 'email' in session:
            sql = "UPDATE `consultation_request` SET `is_accepted_mentor`=%s WHERE `id`=%s"
            data = (is_accepted_mentor, user_id)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify({'message' : 'Consultation status updated'})
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

# profile
@app.route('/profile/individual/<int:id>', methods=['GET'])
def individualProfile(id):
    try:
        if 'email' in session:
            sql = "select id, name, email, user_id from individual_main where id = %s"
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

@app.route('/profile/mentor/<int:id>', methods=['GET'])
def mentorProfile(id):
    try:
        if 'email' in session:
            sql = "select id, name, email, user_id, linkedin_link, experience, jobtitle, company, rate_per_hour, agreement_pdf from mentor_main where id = %s"
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

@app.route('/profile/corporate/<int:id>', methods=['GET'])
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

@app.route('/profile/individual/<int:id>', methods=['PUT'])
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

@app.route('/profile/mentor/<int:user_id>', methods=['PUT'])
def updateMentorProfile(user_id):
    return jsonify({'message' : 'Profile updated'})

@app.route('/profile/corporate/<int:user_id>', methods=['PUT'])
def updateCorporateProfile(user_id):
    return jsonify({'message' : 'Profile updated'})

# Consultation
@app.route('/consultation', methods=['POST'])
def consultationSession():
    try:
        data = request.form
        requestorId = data['requestor_id']
        mentorId = data['mentor_id']
        consultationDate = data['consultation_date']
        startTime = data['start_time']
        endTime = data['end_time']
        if 'email' in session:
            sql = "INSERT INTO `consultation_request` (`requestor_id`, `mentor_id`, `consultation_date`, `start_time`, `end_time`) VALUES (%s,%s,%s,%s,%s)"
            data = (requestorId, mentorId, consultationDate, startTime, endTime)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify({'message' : 'Consultation session created'})
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

@app.route('/consultation/payment/<int:consult_id>', methods=['PUT'])
def consultationSessionPayment(consult_id):
    try:
        data = request.form
        payment_status = data['payment_status']
        if 'email' in session:
            sql = "UPDATE `consultation_request` SET `payment_status`=%s WHERE `id`=%s"
            data = (payment_status, consult_id)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify({'message' : 'Consultation session payment updated'})
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

@app.route('/consultation/accept/', methods=['POST'])
def consultationSessionAccept():
    try:
        data = request.form
        consultationReqId = data['consultation_req_id']
        linkZoom = data['link_zoom']
        if 'email' in session:
            sql = "insert into acc_consultation_req (consultation_req_id, link_zoom) values (%s, %s)"
            data = (consultationReqId, linkZoom)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            response = jsonify({'message' : 'Consultation session accepted'})
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

@app.errorhandler(404)
def otherRoutes(error=None):
    response = jsonify({'status': 404, 'message': 'Not Found:'+request.url, })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)
