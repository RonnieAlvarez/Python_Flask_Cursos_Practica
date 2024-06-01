import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://edteamdb:!Soporte06@localhost:5432/edteamdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # DATABASE_URL="postgresql+psycopg2://postgresql:!Soporte06@localhost:5432/edteamdb"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    