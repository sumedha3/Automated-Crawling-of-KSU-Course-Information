from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from Application.models import User
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError

# get all courses
from pymongo import MongoClient
# Connect to the MongoDB server running on localhost
client = MongoClient()
# Access the course_info database
db = client.course_info
# Access the course_info collection
collection = db.course_info
# Retrieve all documents in the collection
courses = collection.find()

# title of the course all courses
course_title = []
for course in courses:
    course_title.append(course['title'].strip())
    
# make list of tuples
course_title = [(course, course) for course in course_title]
    
#print(course_title)

class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
    

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    previous_courses = SelectField("Previous Courses", choices=course_title)
    education_level = SelectField("Education Level", choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')])
    grade = StringField("Grade") #A drop down menu would be bette
    grade = SelectField("Grade", choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    score = FloatField("Score")
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please choose a different email address.")


    