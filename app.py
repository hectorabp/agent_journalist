from flask import Flask
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from routes.links_routes import links_blueprint
from routes.notes_txt_routes import notes_txt_blueprint
from routes.categories_routes import categories_blueprint
from routes.web_routes import web_blueprint

def create_app():
    app = Flask(__name__)

    # Registrar los Blueprints
    app.register_blueprint(links_blueprint, url_prefix="/")
    app.register_blueprint(notes_txt_blueprint, url_prefix="/")
    app.register_blueprint(categories_blueprint, url_prefix="/")
    app.register_blueprint(web_blueprint, url_prefix="/")
    return app

# Iniciar la aplicación
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
