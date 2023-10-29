from flask import Blueprint, render_template

# Initialize the blueprint
app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')
