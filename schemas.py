from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactoBase(BaseModel):
    cliente_id: str
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    mensaje: str
    cf_turnstile_response: str

class ReservaBase(BaseModel):
    cliente_id: str
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    fecha_reserva: str  # YYYY-MM-DD
    hora_reserva: str    # HH:MM
    personas: Optional[int] = None
    comentarios: Optional[str] = None
    cf_turnstile_response: str

class CotizacionBase(BaseModel):
    cliente_id: str
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    servicio: Optional[str] = None
    descripcion: Optional[str] = None
    presupuesto: Optional[str] = None
    cf_turnstile_response: str