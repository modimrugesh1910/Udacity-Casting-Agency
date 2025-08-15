import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg://postgres:abcdefgh@localhost:5432/agency')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    ALGORITHMS = ["RS256"]
