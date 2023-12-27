import os
from Application import app, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from Application.models import User, Enrollment, course_info 
from Application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from Application.course_list import course_list

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
# couseData = Course.objects.all()

#######################################

@api.route('/api','/api/')
class GetAndPost(Resource):

    #GET ALL 
    def get(self): 
        return jsonify(User.objects.all())

    #POST
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    #GET ONE
    def get(self,idx):
        return jsonify(User.objects(user_id=idx))
        
    #PUT
    def put(self,idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx)) 
        
    #DELETE
    def delete(self,idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

#######################################

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True )

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/enrollment/")
@app.route("/enrollment/<term>")
def courses(term = None):
    if term is None:
        term = "Fall 2023"
    classes = course_info.objects.order_by("-code")
    return render_template("courses.html", courseData=classes, courses = True, term=term )

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        previous_courses = form.previous_courses.data
        education_level = form.education_level.data
        grade = form.grade.data
        score = form.score.data
        # user = User(user_id=user_id,email=email, first_name=first_name, last_name=last_name,education_level=education_level, grade=grade, score=score )
        user = User(user_id=user_id,email=email, first_name=first_name, last_name=last_name,education_level=education_level, grade=grade, score=score, previous_courses=previous_courses )
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/courses", methods=["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    code = request.form.get('code')
    title = request.form.get('title')
    user_id = session.get('user_id')
     
    if code:
        if Enrollment.objects(user_id=user_id,code=code):
            flash(f"Oops! You are already registered in this course {title}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id,code=code).save()
            flash(f"You are enrolled in {title}!", "success")
             
    user = User.objects.get(user_id=user_id)
    if user.education_level == 'UG':
        classes = []
        AVLclasses = course_info.objects.order_by("-code")
    else:
        previous_courses = user.previous_courses
        classes = [previous_courses]
        AVLclasses = course_info.objects(code__in=previous_courses).order_by("-code")
        # classes = course_info.objects(code__in=user.eligible_courses).order_by("-code")
     
    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes, AVLclasses=AVLclasses, current_user=user)



@app.route("/user")
def user():
     #User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
     #User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()
    #  users = User.objects.all()
    #  return render_template("user.html", users=users)   
    # only for current user
    user_id = session.get('user_id')
    # print(user_id)
    if user_id:
        user = User.objects.get(user_id=user_id)
        return render_template("user.html", user=user)
    
    return redirect(url_for('login'))
 
@app.route('/display_visuals')
def display_visuals():
    visuals = []
    # print current working directory
    print(os.getcwd())
    dire = os.getcwd() + "\Application\static\Visual"
    # check if directory exists
    if os.path.exists(dire):
        print("Directory exists")
    # direc = os.getcwd() + '\application\public\static\Visual'
    for filename in os.listdir(dire):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            visuals.append(url_for('static', filename=f'visual/{filename}'))
    return render_template('visual.html', visuals=visuals)

# endpoint to set the enrollment 
@app.route('/set_enrollment', methods=['POST'])
def set_enrollment():
    user_id = request.form.get('user_id')
    code = request.form.get('code')
    course = course_info.objects.get(code=code)
    user = User.objects.get(user_id=user_id)
    if course.code in user.eligible_courses:
        user.update(add_to_set__enrolled_courses=course)
        flash(f"You are enrolled in {course.title}!", "success")
    else:
        flash(f"Oops! You are not eligible to enroll in {course.title}!", "danger")
    return redirect(url_for('student', id=user_id))