from app import db
from app.models import User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime

# Sample data
users_data = [
    {
        "username": "johndoe",
        "password": "password",
        "fullname": "John Doe",
        "qualification": "B.Tech",
        "dob": datetime(1990, 1, 1)
    },
    {
        "username": "janedoe",
        "password": "password",
        "fullname": "Jane Doe",
        "qualification": "M.Tech",
        "dob": datetime(1992, 1, 1)
    },
    {
        "username": "bobsmith",
        "password": "password",
        "fullname": "Bob Smith",
        "qualification": "B.Sc",
        "dob": datetime(1995, 1, 1)
    },
]

subjects_data = [
    {
        "name": "Mathematics",
        "description": "Mathematics subject"
    },
    {
        "name": "Science",
        "description": "Science subject"
    },
]

chapters_data = [
    {
        "name": "Algebra",
        "description": "Algebra chapter",
        "subject_id": 1
    },
    {
        "name": "Biology",
        "description": "Biology chapter",
        "subject_id": 2
    },
]

quizzes_data = [
    {
        "name": "Quiz 1",
        "date_of_quiz": datetime(2024, 1, 1),
        "time_duration": 10*60,
        "chapter_id": 1
    },
    {
        "name": "Quiz 2",
        "date_of_quiz": datetime(2024, 1, 15),
        "time_duration": 10*60,
        "chapter_id": 2
    },
]

questions_data = [
    {
        "question_statement": "What is 2 + 2?",
        "option1": "3",
        "option2": "4",
        "option3": "5",
        "option4": "6",
        "correct_option": 2,
        "quiz_id": 1
    },
    {
        "question_statement": "What is the capital of France?",
        "option1": "Paris",
        "option2": "London",
        "option3": "Berlin",
        "option4": "Rome",
        "correct_option": 1,
        "quiz_id": 1
    },
    {
        "question_statement": "What is the largest planet in our solar system?",
        "option1": "Earth",
        "option2": "Saturn",
        "option3": "Jupiter",
        "option4": "Uranus",
        "correct_option": 3,
        "quiz_id": 1
    },
    {
        "question_statement": "Who painted the Mona Lisa?",
        "option1": "Leonardo da Vinci",
        "option2": "Michelangelo",
        "option3": "Raphael",
        "option4": "Caravaggio",
        "correct_option": 1,
        "quiz_id": 2
    },
    {
        "question_statement": "What is the chemical symbol for gold?",
        "option1": "Ag",
        "option2": "Au",
        "option3": "Hg",
        "option4": "Pb",
        "correct_option": 2,
        "quiz_id": 2
    },
    {
        "question_statement": "What is the smallest country in the world?",
        "option1": "Vatican City",
        "option2": "Monaco",
        "option3": "Nauru",
        "option4": "Tuvalu",
        "correct_option": 1,
        "quiz_id": 2
    },
]

attempts_data = [
    {"user_id": 1, "quiz_id": 1, "total_scored": 2},
    {"user_id": 1, "quiz_id": 2, "total_scored": 3},
    {"user_id": 2, "quiz_id": 1, "total_scored": 1},
    {"user_id": 2, "quiz_id": 2, "total_scored": 2},
    {"user_id": 3, "quiz_id": 1, "total_scored": 3},
    {"user_id": 3, "quiz_id": 2, "total_scored": 2},
]

def seed_database():
    # Add users
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            fullname=user_data["fullname"],
            qualification=user_data["qualification"],
            dob=user_data["dob"]
        )
        user.set_password(user_data["password"])
        db.session.add(user)
    
    # Add subjects
    for subject_data in subjects_data:
        subject = Subject(
            name=subject_data["name"],
            description=subject_data["description"]
        )
        db.session.add(subject)
    
    # Add chapters
    for chapter_data in chapters_data:
        chapter = Chapter(
            name=chapter_data["name"],
            description=chapter_data["description"],
            subject_id=chapter_data["subject_id"]
        )
        db.session.add(chapter)
    
    # Add quizzes
    for quiz_data in quizzes_data:
        quiz = Quiz(
            name=quiz_data["name"],
            date_of_quiz=quiz_data["date_of_quiz"],
            time_duration=quiz_data["time_duration"],
            chapter_id=quiz_data["chapter_id"]
        )
        db.session.add(quiz)
    
    # Add questions
    for question_data in questions_data:
        question = Question(
            question_statement=question_data["question_statement"],
            option1=question_data["option1"],
            option2=question_data["option2"],
            option3=question_data["option3"],
            option4=question_data["option4"],
            correct_option=question_data["correct_option"],
            quiz_id=question_data["quiz_id"]
        )
        db.session.add(question)
    
    # Add attempts
    for attempt_data in attempts_data:
        attempt = Score(
            user_id=attempt_data["user_id"],
            quiz_id=attempt_data["quiz_id"],
            total_scored=attempt_data["total_scored"]
        )
        db.session.add(attempt)
    
    db.session.commit()
