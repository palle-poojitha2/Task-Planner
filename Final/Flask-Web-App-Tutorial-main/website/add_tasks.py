from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db
from datetime import datetime

add_tasks = Blueprint('add_tasks', __name__, template_folder='templates', static_folder='static')

def create_task(title, description, due_date, priority):
    new_task = Task(title=title, description=description, due_date=due_date, priority=priority, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()

def parse_due_date(due_date_str):
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        return due_date
    except ValueError:
        return None

@add_tasks.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority')

        due_date = parse_due_date(due_date_str)

        if due_date is None:
            flash('Invalid due date format. Please use YYYY-MM-DD.', category='error')
        else:
            create_task(title, description, due_date, priority)
            flash('Task added!', category='success')

        # Redirect back to the same "Add New Task" page
        return redirect(request.url)

    return render_template('add_tasks.html', user=current_user)
