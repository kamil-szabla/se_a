# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-no-one-will-guess-lol'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgresql_sea_ksszabla_user:xZR9KMnmlwUga1Z1aXguBr3H54zJSv8n@dpg-crqmcqdsvqrc73d1rsbg-a.frankfurt-postgres.render.com/postgresql_sea_ksszabla')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
