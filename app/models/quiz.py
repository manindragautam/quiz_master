from app import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_quiz = db.Column(db.DateTime)
    time_duration = db.Column(db.Integer, default=0)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

    questions = db.relationship('Question', backref='quiz', lazy=True)
    scores = db.relationship('Score', backref='quiz', lazy=True)