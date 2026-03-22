from flask import Blueprint, request, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
from flask import render_template_string
from models import db, Cliente, Contacto, Reserva, Cotizacion, Post
from datetime import datetime

ADMIN_PANEL_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Blog - Esmeralda</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #f5f5f5;
            padding: 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #c5a572;
            margin-bottom: 2rem;
        }
        h2 {
            color: #c5a572;
            margin: 2rem 0 1rem;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.3rem;
            font-weight: bold;
        }
        input, textarea, select {
            width: 100%;
            padding: 0.5rem;
            background: #2e2e2e;
            border: 1px solid #c5a572;
            color: #fff;
            border-radius: 4px;
            font-family: monospace;
        }
        button {
            background: #c5a572;
            color: #0a0a0a;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-weight: bold;
            border-radius: 4px;
            transition: background 0.3s;
        }
        button:hover {
            background: #d4af37;
        }
        .post-list {
            margin-top: 2rem;
        }
        .post-item {
            background: #1e1e1e;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .post-info {
            flex: 1;
        }
        .post-info h3 {
            margin-bottom: 0.2rem;
        }
        .post-info p {
            color: #aaa;
            font-size: 0.9rem;
        }
        .post-actions {
            display: flex;
            gap: 0.5rem;
        }
        .btn-edit, .btn-delete {
            padding: 0.3rem 0.8rem;
            font-size: 0.8rem;
        }
        .btn-delete {
            background: #b91c1c;
        }
        .btn-delete:hover {
            background: #991b1b;
        }
        .error {
            color: #e74c3c;
            margin-top: 0.5rem;
        }
        .success {
            color: #2ecc71;
            margin-top: 0.5rem;
        }
        hr {
            margin: 2rem 0;
            border-color: #333;
        }
        textarea {
            font-family: monospace;
            min-height: 200px;
        }
        .loading {
            text-align: center;
            padding: 2rem;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Panel de Blog | Esmeralda</h1>

        <!-- Formulario para crear/editar -->
        <div id="form-container">
            <h2 id="form-title">Crear nuevo post</h2>
            <form id="post-form">
                <input type="hidden" id="post-id" name="id">
                <div class="form-group">
                    <label for="titulo">Título *</label>
                    <input type="text" id="titulo" name="titulo" required>
                </div>
                <div class="form-group">
                    <label for="slug">Slug (URL amigable) *</label>
                    <input type="text" id="slug" name="slug" required placeholder="ej: mi-primer-post">
                </div>
                <div class="form-group">
                    <label for="resumen">Resumen *</label>
                    <textarea id="resumen" name="resumen" rows="3" required></textarea>
                </div>
                <div class="form-group">
                    <label for="contenido">Contenido (HTML o Markdown) *</label>
                    <textarea id="contenido" name="contenido" rows="10" required></textarea>
                </div>
                <div class="form-group">
                    <label for="imagen_destacada">URL imagen destacada</label>
                    <input type="url" id="imagen_destacada" name="imagen_destacada" placeholder="https://...">
                </div>
                <div class="form-group">
                    <label for="autor">Autor</label>
                    <input type="text" id="autor" name="autor" value="Ismael Palencia">
                </div>
                <div class="form-group">
                    <label for="cliente_id">Cliente ID (opcional, dejar vacío para posts generales)</label>
                    <input type="text" id="cliente_id" name="cliente_id" placeholder="ej: taller-aguila">
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="publicado" name="publicado" checked> Publicado
                    </label>
                </div>
                <button type="submit" id="submit-btn">Crear post</button>
                <button type="button" id="cancel-btn" style="display:none;">Cancelar</button>
            </form>
            <div id="form-message"></div>
        </div>

        <hr>

        <h2>Posts existentes</h2>
        <div id="posts-list" class="post-list">
            <div class="loading">Cargando posts...</div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin + '/admin';  // ej: https://esmeralda.up.railway.app/admin
        let editingId = null;

        // Helper para hacer fetch con credenciales automáticas (Basic Auth ya está en la sesión)
        async function apiFetch(url, options = {}) {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...(options.headers || {})
                },
                credentials: 'same-origin'  // envía cookies/credenciales
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.error || 'Error en la petición');
            }
            return response.json();
        }

        // Cargar lista de posts
        async function loadPosts() {
            const container = document.getElementById('posts-list');
            container.innerHTML = '<div class="loading">Cargando posts...</div>';
            try {
                const data = await apiFetch(`${API_BASE}/posts`);
                if (!data.length) {
                    container.innerHTML = '<p>No hay posts aún. ¡Crea el primero!</p>';
                    return;
                }
                let html = '';
                data.forEach(post => {
                    html += `
                        <div class="post-item" data-id="${post.id}">
                            <div class="post-info">
                                <h3>${escapeHtml(post.titulo)}</h3>
                                <p>Slug: ${escapeHtml(post.slug)} | ${new Date(post.fecha_publicacion).toLocaleString()}</p>
                                <p>Publicado: ${post.publicado ? '✅ Sí' : '❌ No'} | Cliente: ${post.cliente_id || 'general'}</p>
                            </div>
                            <div class="post-actions">
                                <button class="btn-edit" onclick="editPost(${post.id})">Editar</button>
                                <button class="btn-delete" onclick="deletePost(${post.id})">Eliminar</button>
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            } catch (error) {
                container.innerHTML = `<p class="error">Error cargando posts: ${error.message}</p>`;
            }
        }

        // Escapar HTML
        function escapeHtml(str) {
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        // Crear o actualizar post
        async function savePost(event) {
            event.preventDefault();
            const form = document.getElementById('post-form');
            const formData = new FormData(form);
            const data = {
                titulo: formData.get('titulo'),
                slug: formData.get('slug'),
                resumen: formData.get('resumen'),
                contenido: formData.get('contenido'),
                imagen_destacada: formData.get('imagen_destacada') || null,
                autor: formData.get('autor') || 'Ismael Palencia',
                cliente_id: formData.get('cliente_id') || null,
                publicado: formData.get('publicado') === 'on'
            };
            const messageDiv = document.getElementById('form-message');
            messageDiv.innerHTML = '<div class="loading">Guardando...</div>';
            try {
                let result;
                if (editingId) {
                    // Actualizar
                    result = await apiFetch(`${API_BASE}/posts/${editingId}`, {
                        method: 'PUT',
                        body: JSON.stringify(data)
                    });
                } else {
                    // Crear
                    result = await apiFetch(`${API_BASE}/posts`, {
                        method: 'POST',
                        body: JSON.stringify(data)
                    });
                }
                messageDiv.innerHTML = `<div class="success">✅ ${result.mensaje}</div>`;
                resetForm();
                loadPosts();
            } catch (error) {
                messageDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }

        // Editar post
        async function editPost(id) {
            try {
                const data = await apiFetch(`${API_BASE}/posts`);
                const post = data.find(p => p.id === id);
                if (!post) throw new Error('Post no encontrado');
                editingId = id;
                document.getElementById('post-id').value = post.id;
                document.getElementById('titulo').value = post.titulo;
                document.getElementById('slug').value = post.slug;
                document.getElementById('resumen').value = post.resumen;
                document.getElementById('contenido').value = post.contenido;
                document.getElementById('imagen_destacada').value = post.imagen_destacada || '';
                document.getElementById('autor').value = post.autor;
                document.getElementById('cliente_id').value = post.cliente_id || '';
                document.getElementById('publicado').checked = post.publicado;
                document.getElementById('form-title').innerText = 'Editar post';
                document.getElementById('submit-btn').innerText = 'Actualizar';
                document.getElementById('cancel-btn').style.display = 'inline-block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch (error) {
                alert('Error al cargar el post: ' + error.message);
            }
        }

        // Eliminar post
        async function deletePost(id) {
            if (!confirm('¿Eliminar este post permanentemente?')) return;
            try {
                await apiFetch(`${API_BASE}/posts/${id}`, { method: 'DELETE' });
                alert('Post eliminado');
                if (editingId === id) resetForm();
                loadPosts();
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        // Resetear formulario
        function resetForm() {
            editingId = null;
            document.getElementById('post-form').reset();
            document.getElementById('post-id').value = '';
            document.getElementById('publicado').checked = true;
            document.getElementById('form-title').innerText = 'Crear nuevo post';
            document.getElementById('submit-btn').innerText = 'Crear post';
            document.getElementById('cancel-btn').style.display = 'none';
            document.getElementById('form-message').innerHTML = '';
        }

        // Event listeners
        document.getElementById('post-form').addEventListener('submit', savePost);
        document.getElementById('cancel-btn').addEventListener('click', resetForm);

        // Cargar posts al iniciar
        loadPosts();
    </script>
</body>
</html>
'''

admin_bp = Blueprint('admin', __name__)
auth = HTTPBasicAuth()

# Obtener credenciales desde la configuración de la app
@auth.verify_password
def verify_password(username, password):
    admin_user = current_app.config['ADMIN_USERNAME']
    admin_pass = current_app.config['ADMIN_PASSWORD']
    if username == admin_user and password == admin_pass:
        return username
    return None

# ------------------ Gestión de clientes ------------------

@admin_bp.route('/clientes', methods=['GET'])
@auth.login_required
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'id': c.id,
        'cliente_id': c.cliente_id,
        'nombre_negocio': c.nombre_negocio,
        'email_notificacion': c.email_notificacion,
        'telefono': c.telefono,
        'direccion': c.direccion,
        'activo': c.activo,
        'created_at': c.created_at.isoformat() if c.created_at else None
    } for c in clientes])

@admin_bp.route('/clientes', methods=['POST'])
@auth.login_required
def crear_cliente():
    data = request.get_json()
    required = ['cliente_id', 'nombre_negocio', 'email_notificacion']
    if not all(k in data for k in required):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar que no exista
    existe = Cliente.query.filter_by(cliente_id=data['cliente_id']).first()
    if existe:
        return jsonify({'error': 'cliente_id ya existe'}), 409

    nuevo = Cliente(
        cliente_id=data['cliente_id'],
        nombre_negocio=data['nombre_negocio'],
        email_notificacion=data['email_notificacion'],
        telefono=data.get('telefono'),
        direccion=data.get('direccion'),
        configuracion=data.get('configuracion', {}),
        activo=data.get('activo', True)
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Cliente creado', 'cliente_id': nuevo.cliente_id}), 201

@admin_bp.route('/clientes/<cliente_id>', methods=['PUT'])
@auth.login_required
def actualizar_cliente(cliente_id):
    cliente = Cliente.query.filter_by(cliente_id=cliente_id).first()
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    data = request.get_json()
    # Actualizar campos permitidos
    if 'nombre_negocio' in data:
        cliente.nombre_negocio = data['nombre_negocio']
    if 'email_notificacion' in data:
        cliente.email_notificacion = data['email_notificacion']
    if 'telefono' in data:
        cliente.telefono = data['telefono']
    if 'direccion' in data:
        cliente.direccion = data['direccion']
    if 'configuracion' in data:
        cliente.configuracion = data['configuracion']
    if 'activo' in data:
        cliente.activo = data['activo']

    db.session.commit()
    return jsonify({'mensaje': 'Cliente actualizado'})

@admin_bp.route('/clientes/<cliente_id>', methods=['DELETE'])
@auth.login_required
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.filter_by(cliente_id=cliente_id).first()
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'mensaje': 'Cliente eliminado'})

# ------------------ Consulta de mensajes ------------------

@admin_bp.route('/clientes/<cliente_id>/mensajes', methods=['GET'])
@auth.login_required
def mensajes_cliente(cliente_id):
    """Retorna todos los mensajes (contacto, reserva, cotización) de un cliente, ordenados por fecha descendente."""
    cliente = Cliente.query.filter_by(cliente_id=cliente_id).first()
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    contactos = Contacto.query.filter_by(cliente_id=cliente_id).all()
    reservas = Reserva.query.filter_by(cliente_id=cliente_id).all()
    cotizaciones = Cotizacion.query.filter_by(cliente_id=cliente_id).all()

    mensajes = []

    for c in contactos:
        mensajes.append({
            'id': c.id,
            'tipo': 'contacto',
            'nombre': c.nombre,
            'email': c.email,
            'telefono': c.telefono,
            'mensaje': c.mensaje,
            'fecha': c.fecha.isoformat() if c.fecha else None,
            'leido': c.leido
        })

    for r in reservas:
        mensajes.append({
            'id': r.id,
            'tipo': 'reserva',
            'nombre': r.nombre,
            'email': r.email,
            'telefono': r.telefono,
            'fecha_reserva': r.fecha_reserva.isoformat() if r.fecha_reserva else None,
            'hora_reserva': str(r.hora_reserva) if r.hora_reserva else None,
            'personas': r.personas,
            'comentarios': r.comentarios,
            'fecha': r.fecha_creacion.isoformat() if r.fecha_creacion else None,
            'leido': r.leido
        })

    for cot in cotizaciones:
        mensajes.append({
            'id': cot.id,
            'tipo': 'cotizacion',
            'nombre': cot.nombre,
            'email': cot.email,
            'telefono': cot.telefono,
            'servicio': cot.servicio,
            'descripcion': cot.descripcion,
            'presupuesto': cot.presupuesto,
            'fecha': cot.fecha_creacion.isoformat() if cot.fecha_creacion else None,
            'leido': cot.leido
        })

    # Ordenar por fecha descendente
    mensajes.sort(key=lambda x: x.get('fecha') or '', reverse=True)
    return jsonify(mensajes)

# ------------------ Marcar mensajes como leídos (por tabla) ------------------

@admin_bp.route('/contactos/<int:id>/leido', methods=['PUT'])
@auth.login_required
def marcar_contacto_leido(id):
    mensaje = Contacto.query.get_or_404(id)
    mensaje.leido = True
    db.session.commit()
    return jsonify({'mensaje': 'Marcado como leído'})

@admin_bp.route('/reservas/<int:id>/leido', methods=['PUT'])
@auth.login_required
def marcar_reserva_leido(id):
    mensaje = Reserva.query.get_or_404(id)
    mensaje.leido = True
    db.session.commit()
    return jsonify({'mensaje': 'Marcado como leído'})

@admin_bp.route('/cotizaciones/<int:id>/leido', methods=['PUT'])
@auth.login_required
def marcar_cotizacion_leido(id):
    mensaje = Cotizacion.query.get_or_404(id)
    mensaje.leido = True
    db.session.commit()
    return jsonify({'mensaje': 'Marcado como leído'})


# ------------------ Gestión de posts ------------------
@admin_bp.route('/posts', methods=['GET'])
@auth.login_required
def listar_posts_admin():
    posts = Post.query.order_by(Post.fecha_publicacion.desc()).all()
    return jsonify([p.to_dict() for p in posts])

@admin_bp.route('/posts', methods=['POST'])
@auth.login_required
def crear_post():
    data = request.get_json()
    required = ['titulo', 'slug', 'resumen', 'contenido']
    if not all(k in data for k in required):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    # Verificar slug único
    if Post.query.filter_by(slug=data['slug']).first():
        return jsonify({'error': 'El slug ya existe'}), 409
    
    nuevo = Post(
        titulo=data['titulo'],
        slug=data['slug'],
        resumen=data['resumen'],
        contenido=data['contenido'],
        imagen_destacada=data.get('imagen_destacada'),
        autor=data.get('autor', 'Ismael Palencia'),
        publicado=data.get('publicado', True),
        cliente_id=data.get('cliente_id')  # opcional
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Post creado', 'post': nuevo.to_dict()}), 201

@admin_bp.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
def actualizar_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    
    if 'titulo' in data:
        post.titulo = data['titulo']
    if 'slug' in data:
        # Verificar que el nuevo slug no exista en otro post
        existente = Post.query.filter(Post.slug == data['slug'], Post.id != id).first()
        if existente:
            return jsonify({'error': 'El slug ya existe'}), 409
        post.slug = data['slug']
    if 'resumen' in data:
        post.resumen = data['resumen']
    if 'contenido' in data:
        post.contenido = data['contenido']
    if 'imagen_destacada' in data:
        post.imagen_destacada = data['imagen_destacada']
    if 'autor' in data:
        post.autor = data['autor']
    if 'publicado' in data:
        post.publicado = data['publicado']
    if 'cliente_id' in data:
        post.cliente_id = data['cliente_id']
    
    db.session.commit()
    return jsonify({'mensaje': 'Post actualizado', 'post': post.to_dict()})

@admin_bp.route('/posts/<int:id>', methods=['DELETE'])
@auth.login_required
def eliminar_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'mensaje': 'Post eliminado'})

@admin_bp.route('/posts/panel', methods=['GET'])
@auth.login_required
def posts_panel():
    """Panel de administración para gestionar posts del blog."""
    return render_template_string(ADMIN_PANEL_HTML)