import datetime
import urllib.request
import pymysql
import json
import os

from flask import request, jsonify, session, render_template, redirect, url_for, send_from_directory
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

@app.route('/getfile')
def getFile():
    root = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(root, 'uploads', 'photo', '7e8de5ce-10d5-4d6d-97cc-788af69e3916065ecd0d83ccf29aec249562473bb303.jpg')
    return send_from_directory('uploads/photo', '7e8de5ce-10d5-4d6d-97cc-788af69e3916065ecd0d83ccf29aec249562473bb303.jpg')
    # return redirect(url_for('photo', filename='uploads/' + '7e8de5ce-10d5-4d6d-97cc-788af69e3916065ecd0d83ccf29aec249562473bb303.jpg'), code=301)


@app.errorhandler(404)
def otherRoutes(error=None):
    response = jsonify({'status': 404, 'message': 'Not Found:'+request.url, })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)
