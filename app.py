from flask import Flask
from main.routes import routes

def create_app():
    # Initialize the core application
    app = Flask(__name__, template_folder='main/templates', static_folder='main')

    # Register blueprints
    app.register_blueprint(routes.app)
    
    return app

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True, port=8010)