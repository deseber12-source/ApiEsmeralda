from flask import Blueprint, request, jsonify, current_app
from models import db, Cliente, Contacto
from services.captcha import verify_turnstile
from services.email import send_email
from schemas import ContactoBase
from pydantic import ValidationError
import threading

contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/contacto', methods=['POST'])
def contacto():
    try:
        data = request.get_json()
        form_data = ContactoBase(**data)
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
    nuevo = Contacto(
        cliente_id=form_data.cliente_id,
        nombre=form_data.nombre,
        email=form_data.email,
        telefono=form_data.telefono,
        mensaje=form_data.mensaje
    )
    db.session.add(nuevo)
    db.session.commit()

    # Preparar correo
    subject = f"Nuevo mensaje de contacto - {cliente.nombre_negocio}"
    body = f"""
Has recibido un nuevo mensaje de contacto:

Nombre: {form_data.nombre}
Email: {form_data.email}
Teléfono: {form_data.telefono or 'No proporcionado'}

Mensaje:
{form_data.mensaje}

--- 
Este mensaje fue enviado desde tu sitio web.
"""

    # Enviar en segundo plano
    app = current_app._get_current_object()
    thread = threading.Thread(target=send_email, args=(
        cliente.email_notificacion,
        subject,
        body,
        None,  # from_email por defecto
        app
    ))
    thread.start()

    return jsonify({'status': 'ok', 'message': 'Mensaje enviado correctamente'}), 200