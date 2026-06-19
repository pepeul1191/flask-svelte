# web/views.py

from flask import Blueprint, render_template

view = Blueprint('web-view', __name__)

@view.route('/', methods=['GET'])
def index():
  locals = {
    'title': 'Home',
    'nav_active': 'home',
    'message': '',
  }
  return render_template('web/index.html', locals=locals)

@view.route('/error/403')
def error_403():
  return render_template('web/403.html')

@view.route('/error/404')
def error_404():
  return render_template('web/404.html'), 404