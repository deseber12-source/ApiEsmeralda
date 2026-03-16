
# 🌟 Esmeralda API v1.5.0

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-green)
![Deploy](https://img.shields.io/badge/Deploy-Railway-purple)

---

## 📑 Tabla de contenidos

- [Arquitectura del sistema](#-arquitectura-del-sistema)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos previos](#-requisitos-previos)
- [Configuración del entorno local](#-configuración-del-entorno-local)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Administración](#-administración-http-basic-auth)
- [Despliegue en Railway](#-despliegue-en-railway)
- [Variables de entorno](#-variables-de-entorno)
- [Pruebas locales](#-probar-localmente-con-curl)
- [Notas de desarrollo vs producción](#-notas-importantes-de-desarrollo-vs-producción)

Backend compartido para **páginas web estáticas de pequeños negocios**.  
Procesa formularios de **contacto**, **reservas** y **cotizaciones**, envía notificaciones por correo y almacena los mensajes en una base de datos.


---

# 🏗 Arquitectura del sistema

El sistema está diseñado con una arquitectura simple y desacoplada para poder reutilizar el backend con múltiples páginas web estáticas.

```
Frontend estático (GitHub Pages)
        ↓
Formulario HTML + JavaScript
        ↓
Esmeralda API (Flask / Railway)
        ↓
Validación (Pydantic)
        ↓
Servicios
   ├── Cloudflare Turnstile (anti‑spam)
   ├── SendGrid (envío de correos)
   └── Base de datos
            ↓
       PostgreSQL (producción)
       SQLite (desarrollo)
```

### Flujo de una solicitud

1. El usuario envía un formulario desde una página web estática.
2. JavaScript envía la petición al endpoint correspondiente (`/api/contacto`, `/api/reserva`, etc.).
3. La API valida los datos usando **Pydantic**.
4. Se verifica el captcha con **Cloudflare Turnstile**.
5. Se guarda el mensaje en la base de datos.
6. Se envía una notificación por correo mediante **SendGrid**.

Esta arquitectura permite que **un solo backend pueda servir a múltiples sitios web** simplemente cambiando el `cliente_id`.

---

# 🚀 Características

- Endpoints para **contacto**, **reservas** y **cotizaciones**
- Validación de datos con **Pydantic**
- Protección contra spam con **Cloudflare Turnstile**
- Envío de correos mediante **SendGrid**
- Almacenamiento en **PostgreSQL** (SQLite en desarrollo)
- Rutas administrativas protegidas con **HTTP Basic Auth**
- Arquitectura **modular y fácil de extender**

---

# 🛠️ Tecnologías

- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Pydantic
- SendGrid
- Cloudflare Turnstile
- PostgreSQL / SQLite
- Railway (despliegue)

---

# 📋 Requisitos previos

Antes de ejecutar el proyecto necesitas:

- **Python 3.9 o superior**
- **pip**
- **Git**
- Cuenta en **Railway**
- Cuenta en **SendGrid**
- Cuenta en **Cloudflare** (para Turnstile)

---

# 🔧 Configuración del entorno local

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/esmeralda-backend.git
cd esmeralda-backend
```

## 2️⃣ Crear y activar entorno virtual

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4️⃣ Crear archivo `.env`

Copia el siguiente contenido y completa con tus credenciales:

```env
SECRET_KEY=una-clave-secreta-muy-segura
DATABASE_URL=sqlite:///app.db
SENDGRID_API_KEY=tu-api-key-de-sendgrid
MAIL_DEFAULT_SENDER=eduardo.palencia@cobrabien.org
TURNSTILE_SECRET_KEY=tu-clave-secreta-de-turnstile
ADMIN_USERNAME=admin
ADMIN_PASSWORD=contraseña-segura
```

## 5️⃣ Ejecutar la aplicación localmente

```bash
python app.py
```

La API estará disponible en:

```
http://localhost:5500
```

---

# 📦 Estructura del proyecto

```
esmeralda-backend/
├── app.py                 # Punto de entrada
├── config.py              # Configuración desde variables de entorno
├── models.py              # Modelos de base de datos
├── schemas.py             # Esquemas Pydantic para validación
├── requirements.txt       # Dependencias
├── Procfile               # Configuración de arranque para Railway
├── .env                   # Variables de entorno (NO subir a git)
├── services/
│   ├── captcha.py         # Verificación de Turnstile
│   └── email.py           # Envío de correos con SendGrid
└── routes/
    ├── contacto.py        # Endpoint /api/contacto
    ├── reserva.py         # Endpoint /api/reserva
    ├── cotizacion.py      # Endpoint /api/cotizacion
    └── admin.py           # Rutas protegidas para administración
```

---

# 📡 Endpoints de la API

## Públicos (sin autenticación)

### POST `/api/contacto`

Campos esperados:

```json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "telefono": "string (opcional)",
  "mensaje": "string",
  "cf_turnstile_response": "string"
}
```

---

### POST `/api/reserva`

Campos esperados:

```json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "telefono": "string (opcional)",
  "fecha_reserva": "YYYY-MM-DD",
  "hora_reserva": "HH:MM",
  "personas": "int (opcional)",
  "comentarios": "string (opcional)",
  "cf_turnstile_response": "string"
}
```

---

### POST `/api/cotizacion`

Campos esperados:

```json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "email",
  "telefono": "string (opcional)",
  "servicio": "string (opcional)",
  "descripcion": "string (opcional)",
  "presupuesto": "string (opcional)",
  "cf_turnstile_response": "string"
}
```

---

# 🔐 Administración (HTTP Basic Auth)

| Método | Ruta | Descripción |
|------|------|-------------|
| GET | /admin/clientes | Lista todos los clientes |
| POST | /admin/clientes | Crea un nuevo cliente |
| PUT | /admin/clientes/<cliente_id> | Actualiza un cliente |
| DELETE | /admin/clientes/<cliente_id> | Elimina un cliente |
| GET | /admin/clientes/<cliente_id>/mensajes | Mensajes de un cliente |
| PUT | /admin/contactos/<id>/leido | Marca contacto como leído |
| PUT | /admin/reservas/<id>/leido | Marca reserva como leída |
| PUT | /admin/cotizaciones/<id>/leido | Marca cotización como leída |

---

# ☁️ Despliegue en Railway

## 1️⃣ Preparar el repositorio

Asegúrate de tener:

- `requirements.txt`
- `Procfile`

El `Procfile` debe contener algo como:

```
web: gunicorn app:create_app() --access-logfile -
```

No incluyas el archivo `.env` en el repositorio.

---

## 2️⃣ Crear proyecto en Railway

1. Inicia sesión en Railway  
2. Haz clic en **New Project**  
3. Selecciona **Deploy from GitHub repo**  
4. Conecta tu repositorio  

---

## 3️⃣ Configurar variables de entorno en Railway

Debes agregar las siguientes variables:

- `SECRET_KEY`
- `DATABASE_URL`
- `SENDGRID_API_KEY`
- `MAIL_DEFAULT_SENDER`
- `TURNSTILE_SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

---

## 4️⃣ Agregar base de datos

En Railway agrega un plugin de **PostgreSQL**.

Railway generará automáticamente la variable:

```
DATABASE_URL
```

---

## 5️⃣ Desplegar

Railway detectará los cambios y desplegará automáticamente.

Tu backend tendrá una URL similar a:

```
https://esmeralda.up.railway.app
```

---

# 🔐 Variables de entorno

| Variable | Descripción | Ejemplo |
|--------|-------------|--------|
| SECRET_KEY | Clave secreta de Flask | una-cadena-aleatoria |
| DATABASE_URL | URL de conexión a la BD | postgresql://usuario:pass@host/db |
| SENDGRID_API_KEY | API Key de SendGrid | SG.xxxxx |
| MAIL_DEFAULT_SENDER | Correo remitente | eduardo.palencia@cobrabien.org |
| TURNSTILE_SECRET_KEY | Clave de Cloudflare Turnstile | 0x4AAAAAAA |
| ADMIN_USERNAME | Usuario admin | admin |
| ADMIN_PASSWORD | Contraseña admin | secreto |

---

# 🧪 Probar localmente con curl

```bash
curl -X POST http://localhost:5500/api/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "taller-aguila",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234",
    "mensaje": "Hola, necesito una cotización",
    "cf_turnstile_response": "dummy"
  }'
```

---

# 🧠 Notas importantes de desarrollo vs producción

Durante el despliegue del proyecto se detectaron varias diferencias entre **entorno local** y **producción**.

Estas son lecciones importantes:

### 1️⃣ Flask vs Gunicorn

En desarrollo se ejecuta con:

```
python app.py
```

Pero en producción Railway utiliza:

```
gunicorn
```

Por eso el `Procfile` es necesario.

---

### 2️⃣ Logs HTTP

Flask muestra logs automáticamente en desarrollo, pero **Gunicorn no muestra access logs por defecto**.

Para verlos se debe usar:

```
--access-logfile -
```

---

### 3️⃣ Versión de Python

Algunas librerías (como **Pydantic**) pueden fallar si la versión de Python en Railway es diferente a la del entorno local.

Por eso es recomendable fijar la versión en el proyecto.

---

### 4️⃣ Diferencia de base de datos

En desarrollo se usa:

```
SQLite
```

En producción se usa:

```
PostgreSQL
```

por medio de la variable:

```
DATABASE_URL
```

---

### 5️⃣ Variables de entorno

En desarrollo se usan desde `.env`.

En Railway deben configurarse en el panel de **Variables**.

---

---

# 🗺 Roadmap del proyecto

Posibles mejoras futuras para **Esmeralda API**:

### Backend

- [ ] Sistema de **rate limiting** para prevenir spam masivo
- [ ] Sistema de **logs estructurados**
- [ ] Panel de administración web
- [ ] Sistema de **API Keys por cliente**

### Infraestructura

- [ ] Contenerización con **Docker**
- [ ] Pipeline de **CI/CD**
- [ ] Monitoreo con logs centralizados

### Funcionalidad

- [ ] Webhooks para integrar con otros sistemas
- [ ] Exportación de mensajes a **CSV**
- [ ] Integración con **WhatsApp Business API**

Este roadmap sirve como guía para evolucionar el backend hacia una **plataforma reutilizable para múltiples sitios web de clientes**.

# 📄 Licencia

Este proyecto es **privado** y de uso exclusivo para el desarrollo de páginas web de **Ismael Palencia**.
