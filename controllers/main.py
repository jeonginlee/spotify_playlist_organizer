from flask import Blueprint,render_template

main = Blueprint('main', __name__, template_folder='templates')
@main.route('/')
def main_route():
    return render_template('start.html')

