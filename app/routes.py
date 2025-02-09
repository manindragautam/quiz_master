from app import create_app, db, login_manager
from flask import render_template, redirect, flash, url_for
from app.forms import RegisterForm, LoginForm
from app.models import User, Subject, Chapter, Quiz, Question, Score
from flask_login import current_user, login_user, login_required, logout_user
import os

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.cli.command('db-create')
def create_db():
    db.create_all()

    # create the admin 
    admin = User.query.filter_by(username=os.getenv('ADMIN_USERNAME')).first()
    if not admin:
        admin = User(
            username=os.getenv('ADMIN_USERNAME'),
            fullname="Quiz Master Admin"
        )
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()
        print("Admin created!")
    else:
        print("Admin already exists!")
    print("Database created!")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=os.getenv('ADMIN_USERNAME')).first()
        if user and user.username == form.username.data and user.check_password(form.password.data):
            login_user(user)
            flash("Admin logged in successfully!", category="success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid Username or Password", category="error")
    return render_template("admin/login.html", form=form)

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    return render_template("admin/dashboard.html")

@app.route("/admin/manage_subjects")
@login_required
def manage_subjects():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    subjects = Subject.query.all()
    return render_template("admin/manage_subjects.html", subjects=subjects)

@app.route("/admin/manage_chapters")
@login_required
def manage_chapters():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    chapters = Chapter.query.all()
    return render_template("admin/manage_chapters.html", chapters=chapters)

@app.route("/admin/manage_quizzes")
@login_required
def manage_quizzes():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    quizzes = Quiz.query.all()
    return render_template("admin/manage_quizzes.html", quizzes=quizzes)

@app.route("/admin/manage_questions")
@login_required
def manage_questions():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    questions = Question.query.all()
    return render_template("admin/manage_questions.html", questions=questions)

@app.route("/admin/manage_users")
@login_required
def manage_users():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    users = User.query.all()
    return render_template("admin/manage_users.html", users=users)

@app.route("/admin/manage_scores")
@login_required
def manage_scores():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash("You don't have permission to access this page", category="error")
        return redirect(url_for("home"))
    scores = Score.query.all()
    return render_template("admin/manage_scores.html", scores=scores)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
                    username=form.username.data,
                    fullname=form.fullname.data,
                    qualification=form.qualification.data,
                    dob=form.dob.data
                )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration is successful!', category="success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', category="success")
            return redirect(url_for('dashboard'))
        else:
            flash("Authentication failed!", category="error")
    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!", category="success")
    return redirect(url_for('login'))