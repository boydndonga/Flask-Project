from . import bp
from flask_login import login_required
from flask import render_template

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html', title='Home')