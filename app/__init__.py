# __init__.py
from flask import Flask

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'
from app import views
