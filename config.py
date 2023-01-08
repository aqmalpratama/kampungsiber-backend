from app import app
from flask_mail import Mail, Message
from flaskext.mysql import MySQL
from flask_cors import CORS
from datetime import timedelta, datetime

# app.config['SECRET_KEY'] = 'kampungsiber-key-dev'
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=20)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dev-kampungsiberdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aqmal.dev81@gmail.com'
app.config['MAIL_PASSWORD'] = 'uglkauqrofjtkaac'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

CORS(app)
# UPLOAD_FOLDER = 'uploads/photo'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024