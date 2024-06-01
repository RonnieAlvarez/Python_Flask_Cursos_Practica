from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, SignupForm, AddCourseForm
from models import db, User,Courses

app = Flask(__name__)
port = 5000
app.config["SECRET_KEY"] = "so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:!Soporte06@localhost:5432/edteamdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route("/")
def index():
    return redirect(url_for('signin'))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = SignupForm()
    if form.validate_on_submit() and request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(firstname=firstname, lastname=lastname, email=email)
        user.set_password(password)
        user.save()
        return redirect(url_for("signin"))
    return render_template("signup.html", form=form)

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.get_by_email(email)
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("signin.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard/user/account")
@login_required
def user_account():
    return render_template("user_account.html")

@app.route("/dashboard/courses/add", methods=["GET", "POST"])
@login_required
def add_courses():
    form = AddCourseForm()
    if form.validate_on_submit():
        professor=request.form["professor"]
        title=request.form["title"]
        description=request.form["description"]
        url=request.form["url"]
        course=Courses(professor=professor,title=title,description=description,url=url,user_login_id=current_user.id)
        course.save()
        return redirect(url_for("dashboard"))
    return render_template("add_course.html", form=form)

@app.route("/dashboard/courses")
@login_required
def courses():
    courses = Courses.get_all()
    return render_template("courses.html", courses=courses)

@app.route("/dashboard/course/delete/<id>")
@login_required
def delete_course(id=None):
    course=Courses.get_by_id(id)
    course.delete()
    return redirect(url_for("courses"))

@app.route("/dashboard/course/update/<id>",methods=["GET","POST"])
@login_required
def update_course(id=None):
    course=Courses.get_by_id(id)
    form=AddCourseForm(obj=course)
    if form.validate_on_submit():
        course.professor = request.form["professor"]
        course.title = request.form["title"]
        course.description = request.form["description"]
        course.url = request.form["url"]
        course.save()
        return redirect(url_for("courses"))
    return render_template('add_course.html',form=form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("signin"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
