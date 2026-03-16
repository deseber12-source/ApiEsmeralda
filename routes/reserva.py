from flask import Blueprint, request, jsonify, current_app
from models import db, Cliente, Reserva
from services.captcha import verify_turnstile
from services.email import send_email
from schemas import ReservaBase
from pydantic import ValidationError
from datetime import datetime
import threading

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reserva', methods=['POST'])
def reserva():
    try:
        data = request.get_json()
        form_data = ReservaBase(**data)
    except ValidationError as e:
        return jsonify({'error': 'Datos inválidos', 'detalles': e.errors()}), 400

    # Verificar captcha
    if not verify_turnstile(form_data.cf_turnstile_response):
        return jsonify({'error': 'Captcha inválido'}), 400

    # Verificar cliente
    cliente = Cliente.query.filter_by(cliente_id=form_data.cliente_id, activo=True).first()
    if not cliente:
        return jsonify({'error': 'Cliente no válido'}), 400

    # Convertir fecha y hora
    try:
        fecha = datetime.strptime(form_data.fecha_reserva, '%Y-%m-%d').date()
        hora = datetime.strptime(form_data.hora_reserva, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Formato de fecha u hora inválido'}), 400

    # Guardar en BD
    nueva = Reserva(
        cliente_id=form_data.cliente_id,
        nombre=form_data.nombre,
        email=form_data.email,
        telefono=form_data.telefono,
        fecha_reserva=fecha,
        hora_reserva=hora,
        personas=form_data.personas,
        comentarios=form_data.comentarios
    )
    db.session.add(nueva)
    db.session.commit()

    # Preparar correo
    subject = f"Nueva solicitud de reserva - {cliente.nombre_negocio}"
    body = f"""
Has recibido una nueva solicitud de reserva:

Nombre: {form_data.nombre}
Email: {form_data.email}
Teléfono: {form_data.telefono or 'No proporcionado'}

Fecha: {form_data.fecha_reserva}
Hora: {form_data.hora_reserva}
Personas: {form_data.personas or 'No especificado'}

Comentarios:
{form_data.comentarios or 'Sin comentarios'}

--- 
Esta solicitud fue enviada desde tu sitio web.
"""

    # Enviar en segundo plano
    app = current_app._get_current_object()
    thread = threading.Thread(target=send_email, args=(
        cliente.email_notificacion,
        subject,
        body,
        None,
        app
    ))
    thread.start()

    return jsonify({'status': 'ok', 'message': 'Reserva enviada correctamente'}), 200