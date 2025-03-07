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
            {"name": "Mathematics", "description": "Quizzes related to mathematics."},
            {"name": "Science", "description": "Quizzes related to science."},
            {"name": "History", "description": "Quizzes related to history."}
        ]

chapters_data = [
            {"name": "Algebra", "description": "Basics of algebra.", "subject_id": 1},
            {"name": "Geometry", "description": "Basics of geometry.", "subject_id": 1},
            {"name": "Physics", "description": "Basics of physics.", "subject_id": 2},
            {"name": "Chemistry", "description": "Basics of chemistry.", "subject_id": 2},
            {"name": "World History", "description": "Overview of world history.", "subject_id": 3}
        ]

quizzes_data = [
            {"name": "Algebra Basics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 1},
            {"name": "Geometry Basics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 2},
            {"name": "Physics Basics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 3},
            {"name": "Chemistry Basics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 4},
            {"name": "World History Basics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 5},
            {"name": "Advanced Algebra", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 1},
            {"name": "Advanced Geometry", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 2},
            {"name": "Advanced Physics", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 3},
            {"name": "Advanced Chemistry", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 4},
            {"name": "Advanced World History", "date_of_quiz": datetime(2024, 1, 1), "time_duration": 10*60, "chapter_id": 5}
        ]

questions_data = [
    # Questions for Quiz 1: Algebra Basics
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
        "question_statement": "What is 3 * 5?",
        "option1": "10",
        "option2": "15",
        "option3": "20",
        "option4": "25",
        "correct_option": 2,
        "quiz_id": 1
    },
    {
        "question_statement": "What is 10 - 4?",
        "option1": "5",
        "option2": "6",
        "option3": "7",
        "option4": "8",
        "correct_option": 2,
        "quiz_id": 1
    },

    # Questions for Quiz 2: Geometry Basics
    {
        "question_statement": "What is the sum of angles in a triangle?",
        "option1": "90 degrees",
        "option2": "180 degrees",
        "option3": "270 degrees",
        "option4": "360 degrees",
        "correct_option": 2,
        "quiz_id": 2
    },
    {
        "question_statement": "What is the area of a square with side length 4?",
        "option1": "8",
        "option2": "12",
        "option3": "16",
        "option4": "20",
        "correct_option": 3,
        "quiz_id": 2
    },

    # Questions for Quiz 3: Physics Basics
    {
        "question_statement": "What is the unit of force?",
        "option1": "Joule",
        "option2": "Newton",
        "option3": "Watt",
        "option4": "Pascal",
        "correct_option": 2,
        "quiz_id": 3
    },
    {
        "question_statement": "What is the speed of light?",
        "option1": "300,000 km/s",
        "option2": "400,000 km/s",
        "option3": "500,000 km/s",
        "option4": "600,000 km/s",
        "correct_option": 1,
        "quiz_id": 3
    },

    # Questions for Quiz 4: Chemistry Basics
    {
        "question_statement": "What is the chemical symbol for water?",
        "option1": "H2O",
        "option2": "CO2",
        "option3": "O2",
        "option4": "N2",
        "correct_option": 1,
        "quiz_id": 4
    },
    {
        "question_statement": "What is the atomic number of carbon?",
        "option1": "6",
        "option2": "7",
        "option3": "8",
        "option4": "9",
        "correct_option": 1,
        "quiz_id": 4
    },

    # Questions for Quiz 5: World History Basics
    {
        "question_statement": "Who was the first President of the United States?",
        "option1": "Thomas Jefferson",
        "option2": "George Washington",
        "option3": "Abraham Lincoln",
        "option4": "John Adams",
        "correct_option": 2,
        "quiz_id": 5
    },
    {
        "question_statement": "In which year did World War II end?",
        "option1": "1943",
        "option2": "1944",
        "option3": "1945",
        "option4": "1946",
        "correct_option": 3,
        "quiz_id": 5
    },

    # Questions for Quiz 6: Advanced Algebra
    {
        "question_statement": "What is the solution to x^2 - 4 = 0?",
        "option1": "x = 2",
        "option2": "x = -2",
        "option3": "x = 2 or x = -2",
        "option4": "x = 4",
        "correct_option": 3,
        "quiz_id": 6
    },
    {
        "question_statement": "What is the derivative of x^3?",
        "option1": "2x^2",
        "option2": "3x^2",
        "option3": "4x^3",
        "option4": "3x^3",
        "correct_option": 2,
        "quiz_id": 6
    },

    # Questions for Quiz 7: Advanced Geometry
    {
        "question_statement": "What is the volume of a sphere with radius 3?",
        "option1": "36π",
        "option2": "72π",
        "option3": "108π",
        "option4": "144π",
        "correct_option": 1,
        "quiz_id": 7
    },
    {
        "question_statement": "What is the Pythagorean theorem?",
        "option1": "a^2 + b^2 = c^2",
        "option2": "a + b = c",
        "option3": "a^2 + b^2 = c",
        "option4": "a + b^2 = c^2",
        "correct_option": 1,
        "quiz_id": 7
    },

    # Questions for Quiz 8: Advanced Physics
    {
        "question_statement": "What is the formula for kinetic energy?",
        "option1": "KE = mv",
        "option2": "KE = 0.5mv^2",
        "option3": "KE = mgh",
        "option4": "KE = Fd",
        "correct_option": 2,
        "quiz_id": 8
    },
    {
        "question_statement": "What is the unit of electric current?",
        "option1": "Volt",
        "option2": "Ampere",
        "option3": "Ohm",
        "option4": "Watt",
        "correct_option": 2,
        "quiz_id": 8
    },

    # Questions for Quiz 9: Advanced Chemistry
    {
        "question_statement": "What is the pH of a neutral solution?",
        "option1": "5",
        "option2": "6",
        "option3": "7",
        "option4": "8",
        "correct_option": 3,
        "quiz_id": 9
    },
    {
        "question_statement": "What is the formula for sulfuric acid?",
        "option1": "H2SO4",
        "option2": "HCl",
        "option3": "HNO3",
        "option4": "H3PO4",
        "correct_option": 1,
        "quiz_id": 9
    },

    # Questions for Quiz 10: Advanced World History
    {
        "question_statement": "Who wrote 'The Communist Manifesto'?",
        "option1": "Karl Marx",
        "option2": "Vladimir Lenin",
        "option3": "Joseph Stalin",
        "option4": "Friedrich Engels",
        "correct_option": 1,
        "quiz_id": 10
    },
    {
        "question_statement": "In which year did the Berlin Wall fall?",
        "option1": "1987",
        "option2": "1988",
        "option3": "1989",
        "option4": "1990",
        "correct_option": 3,
        "quiz_id": 10
    }
]

attempts_data = [
    {"user_id": 2, "quiz_id": 1, "total_scored": 3},
    {"user_id": 2, "quiz_id": 2, "total_scored": 3},
    {"user_id": 3, "quiz_id": 1, "total_scored": 1},
    {"user_id": 3, "quiz_id": 2, "total_scored": 2},
    {"user_id": 4, "quiz_id": 1, "total_scored": 2},
    {"user_id": 4, "quiz_id": 2, "total_scored": 2},
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
