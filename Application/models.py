import flask
from Application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()
    # previous_courses = db.ListField(db.StringField())
    education_level = db.StringField(choices=['UG', 'PG'])
    if education_level != 'UG':
        previous_courses = db.StringField()
        grade = db.StringField(max_length=10) 
        score = db.FloatField()
    else:
        # set all 3 to None
        previous_courses = "Not AApplicable"
        grade = "Not AApplicable"
        score = "Not AApplicable"
    eligible_courses = db.ListField(db.StringField())

    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class course_info(db.Document):
    id = db.StringField(primary_key=True)
    code = db.StringField(max_length=10)
    craditHour = db.StringField(max_length=10)
    title = db.StringField(max_length=200)
    description = db.StringField()


class Enrollment(db.Document):
    user_id = db.IntField()
    course_info = db.ReferenceField('course_info', dbref=True)
