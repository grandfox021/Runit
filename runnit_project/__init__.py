from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import secrets


app = Flask(__name__,template_folder="templates")

app.secret_key =secrets.token_hex(16)
DEFAULT_IMAGE_PATH = 'static/uploads/default_pic/default.jpg'  # Define the default image path
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hbsmtp635@gmail.com'
app.config['MAIL_PASSWORD'] = 'ylgt aavy aawr gwwg'
app.config['MAIL_DEFAULT_SENDER'] = 'hbsmtp635@gmail.com'


from runnit_project import routes