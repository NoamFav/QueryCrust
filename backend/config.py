# config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///Database.sql')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    SESSION_TYPE = 'filesystem' 
    #SESSION_PERMANENT = True
    #PERMANENT_SESSION_LIFETIME = timedelta(days=1)  # Duration for session to persist 
