from flask import Blueprint, render_template
from flask_login import login_required, current_user
from numpy import random
import matplotlib.pyplot as plt

analyticss = Blueprint('analytics', __name__, template_folder='templates', static_folder='static')

@analyticss.route('/analytics', methods=['GET'])
@login_required
def analytics():
   

    # Pass the chart path to the template
    return render_template('analytics.html', user=current_user)

