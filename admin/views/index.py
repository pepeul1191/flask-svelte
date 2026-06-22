# admin/views/index.py
from flask import Blueprint, flash, redirect, render_template, request, session
from admin.configs.middlewares import only_logged

views = Blueprint('admin-index-views', __name__, template_folder='../templates')

@views.route('/admin', methods=["GET"])
@only_logged
def index():
  locals = {
    'title': 'Home',
    'nav_link': 'home',
    'message': '',
  }
  return render_template('admin_index.html', locals=locals)