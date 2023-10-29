from flask import Flask
from main.routes import routes
from main.models import convert_model_to_json

def create_app():
    # Initialize the core application
    app = Flask(__name__, template_folder='main/templates', static_folder='main')

    # Load models and convert them to JSON
    convert_model_to_json()

    # Register blueprints
    app.register_blueprint(routes.app)
    
    return app

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True, port=8010)