from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db, Cliente, Contacto, Reserva, Cotizacion, Post
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

    @app.route('/')
    def home():
        return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Esmeralda API - Documentación</title>
    <style>
        body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #f5f5f5;
            padding: 2rem;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: #1e1e1e;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        h1 {
            color: #c5a572;
            border-bottom: 2px solid #c5a572;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
        h2 {
            color: #d4af37;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        h3 {
            color: #c5a572;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
        a {
            color: #d4af37;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            background: #2e2e2e;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
        }
        pre {
            background: #2e2e2e;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-family: monospace;
            font-size: 0.9rem;
        }
        .endpoint {
            background: #2a2a2a;
            border-left: 3px solid #c5a572;
            padding: 0.8rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .method {
            font-weight: bold;
            color: #c5a572;
        }
        footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.8rem;
            color: #888;
            border-top: 1px solid #333;
            padding-top: 1rem;
        }
        .version {
            font-size: 0.8rem;
            color: #888;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Esmeralda API</h1>
        <div class="version">v1.5.0</div>

        <p>
            Backend compartido para páginas web estáticas.
            Procesa formularios de contacto, reservas, cotizaciones y leads.
        </p>

        <h2>📡 Endpoints públicos</h2>

        <div class="endpoint">
            <span class="method">POST</span> <code>/api/contacto</code>
            <p>Envía un mensaje de contacto general.</p>
            <details>
                <summary>Ejemplo de cuerpo (JSON)</summary>
                <pre>{
  "cliente_id": "ejemplo",
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "5551234567",
  "mensaje": "Hola, necesito información",
  "cf_turnstile_response": "token"
}</pre>
            </details>
        </div>

        <div class="endpoint">
            <span class="method">POST</span> <code>/api/reserva</code>
            <p>Crea una nueva reserva (restaurantes, citas).</p>
            <details>
                <summary>Campos adicionales</summary>
                <pre>{
  "fecha_reserva": "2025-03-25",
  "hora_reserva": "20:00",
  "personas": 4,
  "comentarios": "Ventana por favor"
}</pre>
            </details>
        </div>

        <div class="endpoint">
            <span class="method">POST</span> <code>/api/cotizacion</code>
            <p>Solicita una cotización.</p>
            <details>
                <summary>Campos adicionales</summary>
                <pre>{
  "servicio": "Diseño web",
  "descripcion": "Necesito un sitio para mi taller",
  "presupuesto": "$5,000 - $8,000"
}</pre>
            </details>
        </div>

        <div class="endpoint">
            <span class="method">POST</span> <code>/api/leads</code>
            <p>Recibe leads (vista previa) con datos mínimos.</p>
            <details>
                <summary>Ejemplo</summary>
                <pre>{
  "nombre_negocio": "Mi negocio",
  "tipo_negocio": "Restaurante",
  "sensacion": "tradición",
  "tiene_logo": false,
  "telefono": "521551234567",
  "email": "cliente@mail.com"
}</pre>
            </details>
        </div>

        <h2>🔒 Endpoints administrativos</h2>
        <p>Requieren autenticación básica (usuario y contraseña).</p>

        <ul>
            <li><code>GET /admin/clientes</code> – Listar clientes</li>
            <li><code>POST /admin/clientes</code> – Crear cliente</li>
            <li><code>GET /admin/clientes/&lt;cliente_id&gt;/mensajes</code> – Ver mensajes</li>
            <li><code>GET /admin/posts</code> – Listar posts del blog</li>
            <li><code>POST /admin/posts</code> – Crear post</li>
            <li><code>PUT /admin/posts/&lt;id&gt;</code> – Actualizar post</li>
            <li><code>DELETE /admin/posts/&lt;id&gt;</code> – Eliminar post</li>
            <li><a href="/admin/posts/panel">📝 Panel de blog (interfaz web)</a></li>
        </ul>

        <h2>📖 Blog</h2>
        <ul>
            <li><code>GET /api/posts</code> – Lista todos los posts publicados</li>
            <li><code>GET /api/posts?cliente_id=xxx</code> – Filtra por cliente</li>
            <li><code>GET /api/posts/&lt;slug&gt;</code> – Obtiene un post por slug</li>
        </ul>

        <h2>🧪 Probar con curl</h2>
        <pre>
curl -X POST https://apiesmaralda.up.railway.app/api/contacto \
  -H "Content-Type: application/json" \
  -d '{"cliente_id":"test","nombre":"Juan","email":"juan@mail.com","mensaje":"Hola","cf_turnstile_response":"dummy"}'
        </pre>

        <footer>
            Desarrollado por Ismael Palencia ·
            <a href="https://ismaelpalencia.com" target="_blank">ismaelpalencia.com</a><br>
            Contacto: eduardo.palencia@cobrabien.org
        </footer>
    </div>
</body>
</html>
        '''

    return app


# Instancia global para Gunicorn
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5500))
    app.run(host='0.0.0.0', port=port, debug=True)