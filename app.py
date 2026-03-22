from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db, Cliente, Contacto, Reserva, Cotizacion, Post # Importamos el modelo Post
from routes.contacto import contacto_bp
from routes.reserva import reserva_bp
from routes.cotizacion import cotizacion_bp
from routes.admin import admin_bp
from routes.blog import blog_bp
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)  # En producción, restringir orígenes
    migrate = Migrate(app, db)

    # Registrar blueprints
    app.register_blueprint(contacto_bp, url_prefix='/api')
    app.register_blueprint(reserva_bp, url_prefix='/api')
    app.register_blueprint(cotizacion_bp, url_prefix='/api')

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/api')

    # ⚠️ IMPORTANTE:
    # Ya NO usamos db.create_all().
    # Todas las tablas se manejarán con migraciones:
    # flask db migrate
    # flask db upgrade

    return app


# Instancia global para Gunicorn
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5500))
    app.run(host='0.0.0.0', port=port, debug=True)