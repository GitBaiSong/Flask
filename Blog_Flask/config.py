#coding:utf8
import os
DEBUG = True

SECRET_KEY = os.urandom(24)

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = 'rootroot'
DATABASE = 'blog_flask'
CHARSET = 'utf8'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USER,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI