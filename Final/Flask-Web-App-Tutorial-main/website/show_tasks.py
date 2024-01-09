from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Task
from datetime import date
from . import db

from flask import Blueprint, render_template

show_taskss = Blueprint('show_tasks', __name__)

@show_taskss.route('/show-tasks')
@login_required
def show_tasks():
    # Query all tasks for the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # Categorize tasks into ongoing, due, and done based on their due dates
    today = date.today()
    ongoing = []
    due = []
    done = []

    for task in tasks:
        if task.due_date < today:
            done.append(task)
        elif task.due_date == today:
            due.append(task)
        else:
            ongoing.append(task)

    return render_template('show_tasks.html', user=current_user, ongoing=ongoing, due=due, done=done)

@show_taskss.route('/mark_task_completed/<int:task_id>', methods=['POST'])
def mark_task_completed(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return '', 204
