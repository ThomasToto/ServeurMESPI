from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = 'test'

app.config['MYSQL_HOST'] = '192.168.33.33'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root_password'
app.config['MYSQL_DB'] = 'MESPI'

from app import views

