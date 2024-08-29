import os

class Config:
   SECRET_KEY = '2fe0b2a9ab8d2be9750e06eb8a11df20'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   MAIL_SERVER = 'smtp.gmail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = os.environ.get('EMAIL_USER')
   MAIL_PASSWORD = os.environ.get('EMAIL_PASS')