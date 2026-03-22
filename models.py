from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre_negocio = db.Column(db.String(100), nullable=False)
    email_notificacion = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    configuracion = db.Column(db.JSON, default={})
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contacto(db.Model):
    __tablename__ = 'contactos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(50), db.ForeignKey('clientes.cliente_id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)


class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(50), db.ForeignKey('clientes.cliente_id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_reserva = db.Column(db.Date, nullable=False)
    hora_reserva = db.Column(db.Time, nullable=False)
    personas = db.Column(db.Integer)
    comentarios = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)


class Cotizacion(db.Model):
    __tablename__ = 'cotizaciones'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(50), db.ForeignKey('clientes.cliente_id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    servicio = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    presupuesto = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)  # para URLs amigables
    resumen = db.Column(db.String(300), nullable=False)  # extracto para listados
    contenido = db.Column(db.Text, nullable=False)  # HTML o Markdown
    imagen_destacada = db.Column(db.String(300))  # URL de imagen
    autor = db.Column(db.String(100), default='Ismael Palencia')
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    publicado = db.Column(db.Boolean, default=True)
    cliente_id = db.Column(db.String(50), db.ForeignKey('clientes.cliente_id'), nullable=True)  # NULL para posts generales (tuyos)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'slug': self.slug,
            'resumen': self.resumen,
            'contenido': self.contenido,
            'imagen_destacada': self.imagen_destacada,
            'autor': self.autor,
            'fecha_publicacion': self.fecha_publicacion.isoformat() if self.fecha_publicacion else None,
            'publicado': self.publicado,
            'cliente_id': self.cliente_id
        }