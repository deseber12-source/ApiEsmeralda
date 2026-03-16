import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    database_url = os.environ.get('DATABASE_URL')

    # Railway sometimes provides postgres:// which SQLAlchemy may not accept
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'secreto')

    # SendGrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Turnstile
    TURNSTILE_SECRET_KEY = os.environ.get('TURNSTILE_SECRET_KEY')