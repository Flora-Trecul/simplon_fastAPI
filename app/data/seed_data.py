from datetime import datetime, timedelta
import random
from faker import Faker
from app.models.models import User, Course, LearningSession, Inscription
from app.core.database import engine
from sqlalchemy.orm import Session


fake = Faker()

db = Session(engine) 

def seed_data():
    # Créer 30 utilisateurs 
    roles = ["apprenant", "formateur", "administrateur"]
    users = []

    for _ in range(30):
        user = User(
            last_name=fake.last_name(),
            first_name=fake.first_name(),
            email=fake.unique.email(),
            role=random.choice(roles),
            inscription_date=datetime.utcnow()
        )
        users.append(user)

    db.add_all(users)
    db.commit()

    # Créer 10 cours
    levels = ["débutant", "intermédiaire", "avancé"]
    courses = []

    for i in range(10):
        course = Course(
            title=fake.catch_phrase(),
            duration=random.randint(20, 60),
            description=fake.text(max_nb_chars=100),
            level=random.choice(levels)
        )
        courses.append(course)

    db.add_all(courses)
    db.commit()

    # Créer 30 sessions ---
    sessions = []

    for _ in range(30):
        course = random.choice(courses)
        start_date = datetime.utcnow() + timedelta(days=random.randint(0, 60))
        end_date = start_date + timedelta(days=random.randint(5, 30))
        session = LearningSession(
            start_date=start_date,
            end_date=end_date,
            max_capacity=random.randint(5, 15),
            course_id=course.id
        )
        sessions.append(session)

    db.add_all(sessions)
    db.commit()

    # Créer des inscriptions aléatoires
    inscriptions = []
    for user in users:
        user_sessions = random.sample(sessions, random.randint(1, 3))
        for s in user_sessions:
            inscription = Inscription(user_id=user.id, session_id=s.id)
            inscriptions.append(inscription)

    db.add_all(inscriptions)
    db.commit()

    db.close()
    print("Base de données remplie")
    
if __name__ == "__main__":
    seed_data()