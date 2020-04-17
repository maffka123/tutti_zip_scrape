from flask import Flask

app = Flask(__name__)
app.secret_key = 'vfif'
app.debug = True

from app import routes