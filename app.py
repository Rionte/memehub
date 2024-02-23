from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import datetime

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'riontesecretkeymemes123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(15), nullable=False, unique=True)
        password = db.Column(db.String(30), nullable=False)
        is_admin = db.Column(db.Boolean, nullable=False, default=False)
        date = db.Column(db.String(50), nullable=True, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Contact(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(15), nullable=False, unique=False)
        title = db.Column(db.String(80), nullable=False, unique=False)
        message = db.Column(db.String(600), nullable=False, unique=False)
        date = db.Column(db.String(50), nullable=True, unique=False, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meme(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80), nullable=False, unique=False)
        path = db.Column(db.String(100), nullable=False, unique=True)
        author_id = db.Column(db.Integer, nullable=False)
        date = db.Column(db.String(50), nullable=True, unique=False, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class RegisterForm(FlaskForm):
        username = StringField(validators=[InputRequired(), Length(min=4, max=15)], render_kw={'placeholder': 'Username'})
        password = PasswordField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'Password'})
        submit = SubmitField("Register")

        def validate_username(self, username):
            existing_user_username = User.query.filter_by(username=username.data).first()
            if existing_user_username:
                flash("That username already exists. Please choose a different one.")
                raise ValidationError("That username already exists. Please choose a different one.")

    class LoginForm(FlaskForm):
        username = StringField(validators=[InputRequired(), Length(min=4, max=15)], render_kw={'placeholder': 'Username'})
        password = PasswordField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'Password'})
        submit = SubmitField("Login")

    class ContactForm(FlaskForm):
        title = StringField(validators=[InputRequired(), Length(min=1, max=80)])
        message = TextAreaField(validators=[InputRequired(), Length(min=1, max=600)])
        submit = SubmitField("Send Message")

    class MemeForm(FlaskForm):
        title = StringField(validators=[InputRequired(), Length(min=1, max=80)])
        image = FileField(validators=[InputRequired()])
        

    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def main():
    isauth = current_user.is_authenticated
    return render_template("home.html", isauth=isauth, username=current_user.username)

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        new_contact = Contact(username=current_user.username, title=form.title.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('main'))

    isauth = current_user.is_authenticated
    return render_template('contact.html', form=form, isauth=isauth, username=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')