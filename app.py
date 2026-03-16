from flask import Flask
from flask_cors import CORS
from config import Config
from models import db, Cliente  # Importamos Cliente aquí
from routes.contacto import contacto_bp
from routes.reserva import reserva_bp
from routes.cotizacion import cotizacion_bp
from routes.admin import admin_bp
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)  # En producción, restringir orígenes

    # Registrar blueprints
    app.register_blueprint(contacto_bp, url_prefix='/api')
    app.register_blueprint(reserva_bp, url_prefix='/api')
    app.register_blueprint(cotizacion_bp, url_prefix='/api')

    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Crear tablas y datos de prueba (solo en desarrollo)
    with app.app_context():
        db.create_all()
        # Cliente de ejemplo (solo en desarrollo)
        if os.environ.get("FLASK_ENV") == "development":
            if not Cliente.query.filter_by(cliente_id='taller-aguila').first():
                test = Cliente(
                    cliente_id='taller-aguila',
                    nombre_negocio='Taller El Águila',
                    email_notificacion='eduardo.palencia@cobrabien.org'  # Cámbialo para pruebas
                )
                db.session.add(test)
                db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5500))
    app.run(host='0.0.0.0', port=port, debug=True)