from flask import Flask,session,request,flash,redirect,render_template,url_for 
from flask_sqlalchemy import SQLAlchemy
import secrets
from werkzeug.security import generate_password_hash,check_password_hash 
from translations import translations
from flask_mailman import Mail,EmailMessage

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


mail = Mail(app)



# User table with one-to-many relationship with Post and Comment
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(150),unique = True , nullable = False)
    phone_number = db.Column(db.String(20),unique = True , nullable = True)
    profile_pic = db.Column(db.String(120), nullable=True) 
    _password = db.Column(db.String(120) , nullable=False)
    is_authenticated =db.Column(db.Boolean, default=False, nullable=False)
    is_admin=db.Column(db.Boolean, default=False, nullable=False)
    is_superuser =db.Column(db.Boolean, default=False, nullable=False)


    def set_auth_true(self) :
        self.is_authenticated = True

    def set_auth_false(self) :
        self.is_authenticated = False

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
    

# Initialize the database
@app.before_request
def create_tables():
    db.create_all()
    if not "language" in session:
        session["language"] = 'fa'



@app.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route("/")
@app.route("/home")
def home() :

    return render_template("home.html")

 
@app.route("/login/",methods = ['POST','GET'])
def login () :

    if "user" in session:
        flash(translations[session['language']]['already_logged_in']) 
        return redirect(url_for("home"))

    if request.method == "POST" and "sign_in" in request.form:
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        # Query the user by username
        user = User.query.filter_by(email = email).first()

        if user:
            print(f"User found: {user.first_name}")  # Debugging
            print(f"Entered password: {password}")  # Debugging

            if user.verify_password(password):
                print("Password matched")  # Debugging
                session['user_id'] = user.id  # Store user_id in session
                session['user'] = user.email
                user.set_auth_true()
                flash(translations[session['language']]['login_successful']) 
                return redirect(url_for("home"))
            else:
                print("Password comparison failed")  # Debugging
                flash(translations[session['language']]['wrong_password']) 
        else:
            print("User not found")  # Debugging
            flash(translations[session['language']]['wrong_username']) 

    return render_template("login.html", translations=translations[session["language"]])



@app.route("/sign-up",methods = ["POST","GET"])
def signup() :
    if "user_id" in session :
        flash(translations[session['language']]['logout_before_signup']) 
        return redirect(url_for('home'))

    if request.method == 'POST' and "sign_up" in request.form :

        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first() :
            flash(translations[session['language']]['username_already_taken'],"info") 
            return redirect(url_for("signup"))

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(first_name=first_name,last_name = last_name ,email = email, password=password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session["user"] = email
        session["user_id"] = new_user.id


        flash(translations[session['language']]['congrats_account_created']) 
        return redirect(url_for("home"))
    else : 
        return render_template("signup.html", translations=translations[session["language"]])



@app.route("/send-email")
def send_email() :
    title = "reset Pass"
    body = "hello this is a message from support to reset your pass please follow"
    sender_email = "hbsmtp635@gmail.com"
    reciever_email = ["person-email"]
    msg = EmailMessage(subject=title,body=body,from_email=sender_email,to=reciever_email)
    msg.send()
    return "message sent successfully check your inbox"




if __name__ == '__main__':
    app.run(debug=True)   