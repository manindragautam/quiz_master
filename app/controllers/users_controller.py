from flask import Blueprint, render_template, redirect, flash, url_for, request
from app import db
from flask_login import current_user, login_required
from random import shuffle
from app.models.chapter import Chapter
from app.models.quiz import Quiz
from app.models.score import Score
from app.models.subject import Subject
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route("/dashboard")
@login_required
def dashboard():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    total_attempted_quizzes = len(scores)

    average_score = sum([s.total_scored for s in scores]) / total_attempted_quizzes if total_attempted_quizzes > 0 else 0

    return render_template("user/dashboard.html",
                           scores=scores,
                           total_attempted_quizzes=total_attempted_quizzes,
                           average_score=average_score)

@users_bp.route("/attempt_quiz/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.copy()
    shuffle(questions)
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer and int(user_answer) == question.correct_option:
                score += 1
        user_score = Score(
            total_scored=score,
            quiz_id=quiz_id,
            user_id=current_user.id
        )
        db.session.add(user_score)
        db.session.commit()
        flash(f'Quiz completed! Your score: {score} / {len(questions)}', category="success")
        return redirect(url_for("users.quiz_results", quiz_id=quiz_id))
    return render_template("user/attempt_quiz.html", quiz=quiz, questions=questions)

@users_bp.route("/quiz_results/<int:quiz_id>")
@login_required
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first()
    return render_template("user/quiz_results.html", quiz=quiz, score=score)

@users_bp.route("/leaderboard")
@login_required
def leaderboard():
    users = User.get_all_users()
    leaderboard_data = []

    for user in users:
        scores = Score.query.filter_by(user_id=user.id).all()
        total_score = sum([s.total_scored for s in scores])
        leaderboard_data.append({
            "user_fullname": user.fullname,
            "total_score": total_score
        })
    leaderboard_data.sort(key=lambda x: x['total_score'], reverse=True)
    user_fullnames = [x['user_fullname'] for x in leaderboard_data]
    user_total_scores = [x['total_score'] for x in leaderboard_data]
    return render_template("user/leaderboard.html",
                           leaderboard_data=leaderboard_data,
                           user_fullnames=user_fullnames,
                           user_total_scores=user_total_scores)

@users_bp.route("/select-quiz", methods=['GET', 'POST'])
@login_required
def select_quiz():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()

    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        chapter_id = request.form.get('chapter_id')

        if subject_id:
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject_id).all()
        if chapter_id:
            quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

    return render_template("user/select-quiz.html",
                           subjects=subjects,
                           chapters=chapters,
                           quizzes=quizzes)