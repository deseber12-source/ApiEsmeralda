from flask import Blueprint, request, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
from models import db, Cliente, Contacto, Reserva, Cotizacion
from datetime import datetime

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
