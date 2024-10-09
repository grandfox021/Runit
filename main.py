from flask import Flask,session,request,flash,redirect,render_template,url_for 
from flask_sqlalchemy import SQLAlchemy
import secrets
from werkzeug.security import generate_password_hash,check_password_hash 
from translations import translations


app = Flask(__name__,template_folder="templates")

app.secret_key =secrets.token_hex(16)
DEFAULT_IMAGE_PATH = 'static/uploads/default_pic/default.jpg'  # Define the default image path
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




# User table with one-to-many relationship with Post and Comment
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150),unique = True , nullable = False)
    _password = db.Column(db.String(120) , nullable=False)
    is_authenticated =db.Column(db.Boolean, default=False, nullable=False)


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

    if "username" in session:
        flash(translations[session['language']]['already_logged_in']) 
        return redirect(url_for("home"))

    if request.method == "POST" and "sign_in" in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Query the user by username
        user = User.query.filter_by(username=username,email = email).first()

        if user:
            print(f"User found: {user.username}")  # Debugging
            print(f"Entered password: {password}")  # Debugging

            if user.verify_password(password):
                print("Password matched")  # Debugging
                session['user_id'] = user.id  # Store user_id in session
                session['username'] = user.username
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

        username = request.form['username']
        if User.query.filter_by(username=username).first() :
            flash(translations[session['language']]['username_already_taken'],"info") 
            return redirect(url_for("signup"))
        email = request.form['email']
        password = request.form['password']
        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(username=username,email = email, password=password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session["username"] = username
        session["user_id"] = new_user.id


        flash(translations[session['language']]['congrats_account_created']) 
        return redirect(url_for("home"))
    else : 
        return render_template("signup.html", translations=translations[session["language"]])





if __name__ == '__main__':
    app.run(debug=True)   