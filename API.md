 Esmeralda API v1.6.0 – Documentación completa
Backend compartido para páginas web estáticas de pequeños negocios. Procesa formularios de contacto, reservas y cotizaciones, gestiona posts de blog, envía notificaciones por correo y almacena los mensajes en una base de datos. Diseñado para ser desplegado en Railway y consumido desde sitios en GitHub Pages.

📋 Tabla de contenidos
Información general

Autenticación

Endpoints públicos

Contacto

Reservas

Cotizaciones

Blog - Listar posts

Blog - Ver post

Endpoints de administración

Clientes

Mensajes

Blog

Modelos de datos

Códigos de respuesta

Ejemplos de uso

Variables de entorno

📌 Información general
URL base: https://tu-backend.up.railway.app/api (desarrollo: http://localhost:5500/api)

Formato: JSON

Métodos: GET, POST, PUT, DELETE

Autenticación para rutas de admin: HTTP Basic Auth

🔐 Autenticación
Las rutas de administración (prefijo /admin) requieren autenticación básica. Las credenciales se configuran mediante variables de entorno:

text
ADMIN_USERNAME=tu_usuario
ADMIN_PASSWORD=tu_contraseña
🌐 Endpoints públicos
POST /api/contacto
Envía un mensaje de contacto general.

Campos requeridos:

json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "mensaje": "string",
  "cf_turnstile_response": "string"
}
Campos opcionales:

json
{
  "telefono": "string"
}
Respuesta exitosa (200):

json
{
  "status": "ok",
  "message": "Mensaje enviado correctamente"
}
POST /api/reserva
Envía una solicitud de reserva o cita.

Campos requeridos:

json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "fecha_reserva": "YYYY-MM-DD",
  "hora_reserva": "HH:MM",
  "cf_turnstile_response": "string"
}
Campos opcionales:

json
{
  "telefono": "string",
  "personas": "integer",
  "comentarios": "string"
}
Respuesta exitosa (200):

json
{
  "status": "ok",
  "message": "Reserva enviada correctamente"
}
POST /api/cotizacion
Envía una solicitud de cotización.

Campos requeridos:

json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "cf_turnstile_response": "string"
}
Campos opcionales:

json
{
  "telefono": "string",
  "servicio": "string",
  "descripcion": "string",
  "presupuesto": "string"
}
Respuesta exitosa (200):

json
{
  "status": "ok",
  "message": "Cotización enviada correctamente"
}
GET /api/posts
Lista los posts publicados. Si se pasa cliente_id, filtra por ese cliente.

Parámetros query:

cliente_id (opcional) – filtra posts de un cliente específico

Respuesta exitosa (200):

json
[
  {
    "id": 1,
    "titulo": "Mi primer post",
    "slug": "mi-primer-post",
    "resumen": "Este es un resumen breve",
    "contenido": "<p>Contenido completo en HTML</p>",
    "imagen_destacada": "https://...",
    "autor": "Ismael Palencia",
    "fecha_publicacion": "2025-03-21T12:00:00",
    "publicado": true,
    "cliente_id": null
  }
]
GET /api/posts/<slug>
Obtiene un post específico por su slug.

Respuesta exitosa (200):

json
{
  "id": 1,
  "titulo": "Mi primer post",
  "slug": "mi-primer-post",
  "resumen": "Este es un resumen breve",
  "contenido": "<p>Contenido completo en HTML</p>",
  "imagen_destacada": "https://...",
  "autor": "Ismael Palencia",
  "fecha_publicacion": "2025-03-21T12:00:00",
  "publicado": true,
  "cliente_id": null
}
Error (404):

json
{
  "error": "Post no encontrado"
}
🛡️ Endpoints de administración (protegidos)
Todos los endpoints de admin requieren autenticación básica.

Gestión de clientes
Método	Ruta	Descripción
GET	/admin/clientes	Lista todos los clientes
POST	/admin/clientes	Crea un nuevo cliente
PUT	/admin/clientes/<cliente_id>	Actualiza un cliente
DELETE	/admin/clientes/<cliente_id>	Elimina un cliente
POST /admin/clientes – Campos requeridos:

json
{
  "cliente_id": "string",
  "nombre_negocio": "string",
  "email_notificacion": "email"
}
Campos opcionales:

json
{
  "telefono": "string",
  "direccion": "string",
  "configuracion": {},
  "activo": true
}
Consulta de mensajes
Método	Ruta	Descripción
GET	/admin/clientes/<cliente_id>/mensajes	Todos los mensajes de un cliente
Respuesta:

json
[
  {
    "id": 1,
    "tipo": "contacto",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234",
    "mensaje": "Hola, necesito información",
    "fecha": "2025-03-21T10:00:00",
    "leido": false
  },
  {
    "id": 2,
    "tipo": "reserva",
    "nombre": "María López",
    "email": "maria@example.com",
    "telefono": "555-5678",
    "fecha_reserva": "2025-03-25",
    "hora_reserva": "20:00",
    "personas": 4,
    "comentarios": "Ventana cerca de la música",
    "fecha": "2025-03-21T11:00:00",
    "leido": true
  }
]
Marcar como leído:

Método	Ruta	Descripción
PUT	/admin/contactos/<id>/leido	Marca contacto como leído
PUT	/admin/reservas/<id>/leido	Marca reserva como leída
PUT	/admin/cotizaciones/<id>/leido	Marca cotización como leída
Gestión de posts del blog
Método	Ruta	Descripción
GET	/admin/posts	Lista todos los posts
POST	/admin/posts	Crea un nuevo post
PUT	/admin/posts/<id>	Actualiza un post
DELETE	/admin/posts/<id>	Elimina un post
POST /admin/posts – Campos requeridos:

json
{
  "titulo": "string",
  "slug": "string",
  "resumen": "string",
  "contenido": "string"
}
Campos opcionales:

json
{
  "imagen_destacada": "string",
  "autor": "string",
  "publicado": true,
  "cliente_id": "string"
}
Panel de administración web:
Accede a https://tu-backend.up.railway.app/admin/posts/panel para una interfaz gráfica de gestión de posts.

📊 Modelos de datos
Cliente
Campo	Tipo	Descripción
id	integer	Clave primaria
cliente_id	string	Identificador único del negocio (ej. "bunker69")
nombre_negocio	string	Nombre comercial
email_notificacion	string	Correo donde llegarán los mensajes
telefono	string	Teléfono de contacto
direccion	string	Dirección física
configuracion	json	Preferencias adicionales
activo	boolean	Si el cliente está habilitado
created_at	datetime	Fecha de creación
Contacto
Campo	Tipo
id	integer
cliente_id	string (FK)
nombre	string
email	string
telefono	string
mensaje	text
fecha	datetime
leido	boolean
Reserva
Campo	Tipo
id	integer
cliente_id	string (FK)
nombre	string
email	string
telefono	string
fecha_reserva	date
hora_reserva	time
personas	integer
comentarios	text
fecha_creacion	datetime
leido	boolean
Cotización
Campo	Tipo
id	integer
cliente_id	string (FK)
nombre	string
email	string
telefono	string
servicio	string
descripcion	text
presupuesto	string
fecha_creacion	datetime
leido	boolean
Post
Campo	Tipo
id	integer
titulo	string
slug	string (unique)
resumen	string
contenido	text
imagen_destacada	string
autor	string
fecha_publicacion	datetime
publicado	boolean
cliente_id	string (FK, nullable)
🔄 Códigos de respuesta
Código	Significado
200	OK – Solicitud exitosa
201	Created – Recurso creado
400	Bad Request – Datos inválidos o faltantes
401	Unauthorized – Autenticación requerida
404	Not Found – Recurso no encontrado
409	Conflict – Recurso ya existe (ej. slug duplicado)
500	Internal Server Error – Error del servidor
📝 Ejemplos de uso
Enviar un mensaje de contacto (curl)
bash
curl -X POST https://tu-backend.up.railway.app/api/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "bunker69",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234",
    "mensaje": "Hola, quiero hacer una reserva",
    "cf_turnstile_response": "token_del_captcha"
  }'
Crear un cliente (admin)
bash
curl -u admin:tu_contraseña -X POST https://tu-backend.up.railway.app/admin/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "bunker69",
    "nombre_negocio": "Bunker 69",
    "email_notificacion": "contacto@bunker69.com",
    "telefono": "55 1234 5678"
  }'
Crear un post (admin)
bash
curl -u admin:tu_contraseña -X POST https://tu-backend.up.railway.app/admin/posts \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Bienvenidos a Bunker 69",
    "slug": "bienvenidos",
    "resumen": "Abrimos nuestras puertas con una nueva propuesta",
    "contenido": "<p>Texto completo del post...</p>",
    "imagen_destacada": "https://images.unsplash.com/...",
    "cliente_id": "bunker69"
  }'
Obtener posts de un cliente
bash
curl https://tu-backend.up.railway.app/api/posts?cliente_id=bunker69
⚙️ Variables de entorno
Variable	Descripción	Obligatoria
SECRET_KEY	Clave secreta de Flask	Sí
DATABASE_URL	URL de conexión a PostgreSQL	Sí
SENDGRID_API_KEY	API Key de SendGrid	Sí (para correos)
MAIL_DEFAULT_SENDER	Correo remitente	Sí (para correos)
TURNSTILE_SECRET_KEY	Clave secreta de Cloudflare Turnstile	Sí
ADMIN_USERNAME	Usuario para rutas admin	Sí
ADMIN_PASSWORD	Contraseña para rutas admin	Sí
📌 Notas importantes
El token de Turnstile se espera en el campo cf_turnstile_response (con guión bajo). El frontend debe renombrarlo antes de enviar.

Los slugs de los posts deben ser únicos y usar solo letras minúsculas, números y guiones (ej. mi-primer-post).

Los mensajes de los formularios se guardan en la base de datos y además se envían por correo al email_notificacion del cliente.

Los posts con cliente_id = null son generales y aparecen en el blog principal. Los posts con cliente_id específico solo se muestran cuando se filtra por ese ID.

¿Necesitas que añada algún detalle más o ajustar algún endpoint?



**Versión:** 1.6.0  
**Última actualización:** 21 de marzo de 2025