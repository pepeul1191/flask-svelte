# web/views.py
from flask import Blueprint, render_template

views = Blueprint('web-views', __name__, template_folder='./templates')

@views.route('/', methods=['GET'])
def index():
  locals = {
    'title': 'Home',
    'nav_active': 'home',
    'message': '',
  }
  return render_template('index.html', locals=locals)

@views.route('/incubadora', methods=['GET'])
def incubadora():
  locals = {
    'title': 'Inncuvadora',
    'nav_active': 'home',
    'message': '',
  }
  return render_template('incubadora.html', locals=locals)

@views.route('/error/403')
def error_403():
  return render_template('403.html')

@views.route('/error/404')
def error_404():
  return render_template('404.html'), 404