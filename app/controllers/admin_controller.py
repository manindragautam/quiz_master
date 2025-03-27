from functools import wraps
from flask import Blueprint, render_template, redirect, flash, request, url_for
from sqlalchemy import and_
from app import db
from app.forms import SubjectForm, ChapterForm, QuizForm, QuestionForm
from flask_login import current_user, login_required
from app.models.chapter import Chapter
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.score import Score
from app.models.subject import Subject
from app.models.user import User

admin_bp = Blueprint('admin', __name__)

def admin_login_required(func):
    @wraps(func)

    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_required(func)(*args, **kwargs)
        
        if not current_user.is_admin:
            flash("You don't have permission to access this page", category="error")
            return redirect(url_for("home"))
        
        return func(*args, **kwargs)
        
    return decorated_view

@admin_bp.route("/admin/dashboard")
@admin_login_required
def admin_dashboard():
    quizzes = Quiz.query.all()
    quiz_names = [quiz.name for quiz in quizzes]
    average_scores = []
    completion_rates = []

    for quiz in quizzes:
        scores = Score.query.filter_by(quiz_id=quiz.id).all()
        if scores:
            average_score = sum([s.total_scored for s in scores]) / len(scores)

            users_attempted = len(scores)
            completion_rate = (users_attempted / (User.query.count() - 1)) * 100
        else:
           average_score = 0 
           completion_rate = 0
        average_scores.append(average_score)
        completion_rates.append(completion_rate)
    return render_template("admin/dashboard.html",
                           quiz_names=quiz_names,
                           average_scores=average_scores,
                           completion_rates=completion_rates)

# SUBJECT ROUTES

@admin_bp.route("/admin/manage_subjects", methods=['GET', 'POST'])
@admin_login_required
def manage_subjects():
    subjects = Subject.query.all()
    query = request.form.get('query', '')

    if request.method == 'POST':
        subjects = Subject.query.filter(
            Subject.name.ilike(f'%{query}%')
        ).all()

    return render_template("admin/subject/manage_subjects.html",
                           query=query, subjects=subjects)

@admin_bp.route("/admin/add_subject", methods=['GET', 'POST'])
@admin_login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash("Subject added successfully!", category="success")
        return redirect(url_for("admin.manage_subjects"))
    return render_template("admin/subject/add_subject.html", form=form)

@admin_bp.route("/admin/edit_subject/<int:id>", methods=['GET', 'POST'])
@admin_login_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash("Subject updated successfully!", category="success")
        return redirect(url_for("admin.manage_subjects"))
    return render_template("admin/subject/edit_subject.html", form=form)

@admin_bp.route("/admin/delete_subject/<int:id>", methods=['POST'])
@admin_login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully!", category="success")
    return redirect(url_for("admin.manage_subjects"))

# CHAPTER ROUTES

@admin_bp.route("/admin/subject/<int:subject_id>/chapters", methods=['GET', 'POST'])
@admin_login_required
def manage_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject:
        chapters = subject.chapters

        query = request.form.get('query', '')

        if request.method == 'POST':
            chapters = Chapter.query.filter(
                and_(
                    Chapter.subject_id == subject_id,
                    Chapter.name.ilike(f'%{query}%')
                )
            ).all()

    else:
        chapters = []
    return render_template("admin/chapter/manage_chapters.html",
                           subject=subject,
                           query=query,
                           chapters=chapters)

@admin_bp.route("/admin/subject/<int:subject_id>/add_chapter", methods=['GET', 'POST'])
@admin_login_required
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.name.data,
            description=form.description.data,
            subject_id=subject_id
        )
        db.session.add(chapter)
        db.session.commit()
        flash("Chapter added successfully!", category="success")
        return redirect(url_for("admin.manage_chapters", subject_id=subject_id))
    return render_template("admin/chapter/add_chapter.html",
                           subject=subject,
                           form=form)

@admin_bp.route("/admin/subject/<int:subject_id>/edit_chapter/<int:chapter_id>", methods=['GET', 'POST'])
@admin_login_required
def edit_chapter(subject_id, chapter_id):
    subject = Subject.query.get_or_404(subject_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm(obj=chapter)
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = subject_id
        db.session.commit()
        flash("Chapter updated successfully!", category="success")
        return redirect(url_for("admin.manage_chapters", subject_id=subject_id))
    return render_template("admin/chapter/edit_chapter.html",
                           subject=subject,
                           form=form)

@admin_bp.route("/admin/subject/<int:subject_id>/delete_chapter/<int:chapter_id>", methods=['POST'])
@admin_login_required
def delete_chapter(subject_id, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully!", category="success")
    return redirect(url_for("admin.manage_chapters", subject_id=subject_id))

# QUIZ ROUTES

@admin_bp.route("/admin/chapter/<int:chapter_id>/quizzes", methods=['GET', 'POST'])
@admin_login_required
def manage_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter:
        quizzes = chapter.quizzes

        query = request.form.get('query', '')

        if request.method == 'POST':
            quizzes = Quiz.query.filter(
                and_(
                    Quiz.chapter_id == chapter_id,
                    Quiz.name.ilike(f'%{query}%')
                )
            ).all()
    else:
        quizzes = []
    return render_template("admin/quiz/manage_quizzes.html",
                           query=query,
                           chapter=chapter,
                           quizzes=quizzes)

@admin_bp.route("/admin/chapter/<int:chapter_id>/add_quiz", methods=['GET', 'POST'])
@admin_login_required
def add_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(
            name=form.name.data,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=form.time_duration.data,
            chapter_id=chapter_id
        )
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz added successfully!", category="success")
        return redirect(url_for("admin.manage_quizzes", chapter_id=chapter.id))
    return render_template("admin/quiz/add_quiz.html",
                           chapter=chapter,
                           form=form)

@admin_bp.route("/admin/chapter/<int:chapter_id>/edit_quiz/<int:quiz_id>", methods=['GET', 'POST'])
@admin_login_required
def edit_quiz(chapter_id, quiz_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)
    if form.validate_on_submit():
        quiz.name = form.name.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = form.time_duration.data
        quiz.chapter_id = chapter_id
        db.session.commit()
        flash("Quiz updated successfully!", category="success")
        return redirect(url_for("admin.manage_quizzes", chapter_id=chapter_id))
    return render_template("admin/quiz/edit_quiz.html",
                           chapter=chapter,
                           form=form)

@admin_bp.route("/admin/chapter/<int:chapter_id>/delete_quiz/<int:quiz_id>", methods=['POST'])
@admin_login_required
def delete_quiz(chapter_id, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully!", category="success")
    return redirect(url_for("admin.manage_quizzes", chapter_id=chapter_id))

# QUESTION ROUTES

@admin_bp.route("/admin/quiz/<int:quiz_id>/questions")
@admin_login_required
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    return render_template("admin/question/manage_questions.html",
                           quiz=quiz,
                           questions=questions)

@admin_bp.route("/admin/quiz/<int:quiz_id>/add_question", methods=['GET', 'POST'])
@admin_login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            question_statement=form.question_statement.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data,
            quiz_id=quiz_id
        )
        db.session.add(question)
        db.session.commit()
        flash("Question added successfully!", category="success")
        return redirect(url_for("admin.manage_questions", quiz_id=quiz_id))
    return render_template("admin/question/add_question.html",
                           form=form,
                           quiz=quiz)

@admin_bp.route("/admin/quiz/<int:quiz_id>/edit_question/<int:question_id>", methods=['GET', 'POST'])
@admin_login_required
def edit_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.question_statement = form.question_statement.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        question.quiz_id = quiz_id
        db.session.commit()
        flash("Question updated successfully!", category="success")
        return redirect(url_for("admin.manage_questions", quiz_id=quiz_id))
    return render_template("admin/question/edit_question.html",
                           form=form,
                           quiz=quiz)

@admin_bp.route("/admin/quiz/<int:quiz_id>/delete_question/<int:question_id>", methods=['POST'])
@admin_login_required
def delete_question(quiz_id, question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", category="success")
    return redirect(url_for("admin.manage_questions", quiz_id=quiz_id))


@admin_bp.route("/admin/manage_users")
@admin_login_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", users=users)