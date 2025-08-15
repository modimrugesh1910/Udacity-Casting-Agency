from app import app
from models import db, Movie, Actor
from datetime import date

# Sample seed data
movies = [
    {"title": "Inception", "release_date": date(2010, 7, 16)},
    {"title": "The Matrix", "release_date": date(1999, 3, 31)},
    {"title": "Interstellar", "release_date": date(2014, 11, 7)},
]

actors = [
    {"name": "Leonardo DiCaprio", "age": 49, "gender": "Male"},
    {"name": "Keanu Reeves", "age": 59, "gender": "Male"},
    {"name": "Jessica Chastain", "age": 47, "gender": "Female"},
]

def seed_data():
    with app.app_context():
        # Drop and recreate tables to start fresh
        db.drop_all()
        db.create_all()

        # Insert Movies
        for movie in movies:
            m = Movie(title=movie["title"], release_date=movie["release_date"])
            db.session.add(m)

        # Insert Actors
        for actor in actors:
            a = Actor(name=actor["name"], age=actor["age"], gender=actor["gender"])
            db.session.add(a)

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
