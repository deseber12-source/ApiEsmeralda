from flask import Blueprint, request, jsonify, current_app
from models import db, Cliente, Cotizacion
from services.captcha import verify_turnstile
from services.email import send_email
from schemas import CotizacionBase
from pydantic import ValidationError
import threading

cotizacion_bp = Blueprint('cotizacion', __name__)

@cotizacion_bp.route('/cotizacion', methods=['POST'])
def cotizacion():
    try:
        data = request.get_json()
        form_data = CotizacionBase(**data)
    except ValidationError as e:
        return jsonify({'error': 'Datos inválidos', 'detalles': e.errors()}), 400

    # Verificar captcha
    if not verify_turnstile(form_data.cf_turnstile_response):
        return jsonify({'error': 'Captcha inválido'}), 400

    # Verificar cliente
    cliente = Cliente.query.filter_by(cliente_id=form_data.cliente_id, activo=True).first()
    if not cliente:
        return jsonify({'error': 'Cliente no válido'}), 400

    # Guardar en BD
    nueva = Cotizacion(
        cliente_id=form_data.cliente_id,
        nombre=form_data.nombre,
        email=form_data.email,
        telefono=form_data.telefono,
        servicio=form_data.servicio,
        descripcion=form_data.descripcion,
        presupuesto=form_data.presupuesto
    )
    db.session.add(nueva)
    db.session.commit()

    # Preparar correo
    subject = f"Nueva solicitud de cotización - {cliente.nombre_negocio}"
    body = f"""
Has recibido una nueva solicitud de cotización:

Nombre: {form_data.nombre}
Email: {form_data.email}
Teléfono: {form_data.telefono or 'No proporcionado'}

Servicio de interés: {form_data.servicio or 'No especificado'}
Presupuesto estimado: {form_data.presupuesto or 'No especificado'}

Descripción:
{form_data.descripcion or 'Sin descripción'}

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

    return jsonify({'status': 'ok', 'message': 'Cotización enviada correctamente'}), 200