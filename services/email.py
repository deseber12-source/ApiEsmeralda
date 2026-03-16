import os
import threading
from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to, subject, body, from_email=None, app=None):
    """Envía un correo usando SendGrid (puede ejecutarse en hilo)."""
    if app:
        with app.app_context():
            _send_email(to, subject, body, from_email)
    else:
        _send_email(to, subject, body, from_email)


def _send_email(to, subject, body, from_email):
    from_email = from_email or current_app.config.get('MAIL_DEFAULT_SENDER')
    api_key = current_app.config.get('SENDGRID_API_KEY')

    if not api_key:
        current_app.logger.error("SENDGRID_API_KEY no configurada")
        return False

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        current_app.logger.info(f"Correo enviado a {to}, status: {response.status_code}")
        return response.status_code == 202
    except Exception as e:
        current_app.logger.error(f"Error enviando correo: {str(e)}")
        return False