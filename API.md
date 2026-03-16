
Versión: 1.5.0
Última actualización: 15 de marzo de 2025
# API Esmeralda v1.5.0

**Descripción:** API backend para la gestión de páginas web estáticas de clientes. Proporciona endpoints para recibir formularios de contacto, reservas y cotizaciones, así como endpoints administrativos para gestionar clientes y consultar mensajes.

**Base URL:**
- Producción: `https://tu-backend.up.railway.app`
- Desarrollo local: `http://localhost:5500`

---

# Autenticación

- **Endpoints públicos:** No requieren autenticación.
- **Endpoints de administración:** Requieren autenticación básica HTTP (usuario y contraseña configurados en el servidor).

**Formato de datos:** Todas las solicitudes y respuestas son en **JSON**.

---

# Endpoints Públicos

## 1. Enviar mensaje de contacto

`POST /api/contacto`

Registra un mensaje de contacto general y envía una notificación por correo al cliente correspondiente.

### Cuerpo de la solicitud

```json
{
  "cliente_id": "string",          
  "nombre": "string",              
  "email": "string",              
  "telefono": "string",           
  "mensaje": "string",            
  "cf_turnstile_response": "string"
}
```

### Respuesta exitosa

**201 Created**

```json
{
  "status": "ok",
  "message": "Mensaje enviado correctamente"
}
```

### Errores comunes

- **400 Bad Request:** Datos inválidos o falta de campos obligatorios.
- **400 Bad Request:** Captcha inválido.
- **400 Bad Request:** Cliente no válido (cliente_id no existe o inactivo).

---

## 2. Enviar reserva

`POST /api/reserva`

Registra una solicitud de reserva (para restaurantes, citas, etc.) y envía notificación por correo.

### Cuerpo de la solicitud

```json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "string",
  "telefono": "string",
  "fecha_reserva": "YYYY-MM-DD",
  "hora_reserva": "HH:MM",
  "personas": "integer",
  "comentarios": "string",
  "cf_turnstile_response": "string"
}
```

### Respuesta exitosa

**201 Created**

```json
{
  "status": "ok",
  "message": "Reserva enviada correctamente"
}
```

---

## 3. Enviar cotización

`POST /api/cotizacion`

Registra una solicitud de cotización y envía notificación por correo.

### Cuerpo de la solicitud

```json
{
  "cliente_id": "string",
  "nombre": "string",
  "email": "string",
  "telefono": "string",
  "servicio": "string",
  "descripcion": "string",
  "presupuesto": "string",
  "cf_turnstile_response": "string"
}
```

### Respuesta exitosa

**201 Created**

```json
{
  "status": "ok",
  "message": "Cotización enviada correctamente"
}
```

---

# Endpoints de Administración (protegidos)

Todos los endpoints bajo `/admin` requieren **autenticación básica HTTP**.

Las credenciales son las definidas en el entorno:

```
ADMIN_USERNAME
ADMIN_PASSWORD
```

---

## 1. Listar clientes

`GET /admin/clientes`

Devuelve la lista de todos los clientes registrados.

### Respuesta exitosa

**200 OK**

```json
[
  {
    "id": 1,
    "cliente_id": "taller-aguila",
    "nombre_negocio": "Taller El Águila",
    "email_notificacion": "eduardo.palencia@cobrabien.org",
    "telefono": "555-1234",
    "direccion": "Dirección del taller",
    "activo": true,
    "created_at": "2025-03-15T19:43:29"
  }
]
```

---

## 2. Crear nuevo cliente

`POST /admin/clientes`

### Cuerpo de la solicitud

```json
{
  "cliente_id": "string",
  "nombre_negocio": "string",
  "email_notificacion": "string",
  "telefono": "string",
  "direccion": "string",
  "configuracion": {},
  "activo": true
}
```

### Respuesta exitosa

**201 Created**

```json
{
  "mensaje": "Cliente creado",
  "cliente_id": "nuevo-cliente"
}
```

### Errores

- **409 Conflict:** `cliente_id` ya existe.

---

## 3. Actualizar cliente

`PUT /admin/clientes/<cliente_id>`

Actualiza los datos de un cliente existente.

### Cuerpo de la solicitud

```json
{
  "nombre_negocio": "Nuevo nombre",
  "email_notificacion": "nuevo@email.com",
  "telefono": "555-5678",
  "direccion": "Nueva dirección",
  "configuracion": {"campo": "valor"},
  "activo": false
}
```

### Respuesta exitosa

**200 OK**

```json
{
  "mensaje": "Cliente actualizado"
}
```

---

## 4. Eliminar cliente

`DELETE /admin/clientes/<cliente_id>`

### Respuesta exitosa

**200 OK**

```json
{
  "mensaje": "Cliente eliminado"
}
```

---

## 5. Obtener todos los mensajes de un cliente

`GET /admin/clientes/<cliente_id>/mensajes`

Devuelve una lista combinada de todos los mensajes (contactos, reservas, cotizaciones) del cliente, ordenados por fecha descendente.

### Respuesta exitosa

**200 OK**

```json
[
  {
    "id": 1,
    "tipo": "contacto",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234",
    "mensaje": "Hola, necesito una cotización",
    "fecha": "2025-03-15T19:43:29",
    "leido": false
  },
  {
    "id": 2,
    "tipo": "reserva",
    "nombre": "María García",
    "email": "maria@example.com",
    "telefono": "555-5678",
    "fecha_reserva": "2025-04-01",
    "hora_reserva": "20:00",
    "personas": 4,
    "comentarios": "Mesa cerca de la ventana",
    "fecha": "2025-03-15T20:00:00",
    "leido": true
  }
]
```

---

## 6. Marcar mensaje de contacto como leído

`PUT /admin/contactos/<id>/leido`

### Respuesta exitosa

**200 OK**

```json
{
  "mensaje": "Marcado como leído"
}
```

---

## 7. Marcar mensaje de reserva como leído

`PUT /admin/reservas/<id>/leido`

### Respuesta exitosa

**200 OK**

```json
{
  "mensaje": "Marcado como leído"
}
```

---

## 8. Marcar mensaje de cotización como leído

`PUT /admin/cotizaciones/<id>/leido`

### Respuesta exitosa

**200 OK**

```json
{
  "mensaje": "Marcado como leído"
}
```

---

# Códigos de error comunes

| Código | Descripción |
|------|-------------|
| 400 | Error de validación (campos faltantes, formato incorrecto) |
| 401 | Falta autenticación o credenciales incorrectas |
| 404 | Recurso no encontrado |
| 409 | Cliente duplicado |
| 500 | Error interno del servidor |

---

# Ejemplos de uso con curl

## Enviar mensaje de contacto

```bash
curl -X POST http://localhost:5500/api/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "ismaelpalencia",
    "nombre": "Cliente Prueba",
    "email": "test@test.com",
    "mensaje": "Hola, quiero información",
    "cf_turnstile_response": "token_de_prueba"
  }'
```

---

## Crear un nuevo cliente (admin)

```bash
curl -u admin:secreto -X POST http://localhost:5500/admin/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "nuevo-negocio",
    "nombre_negocio": "Mi Nuevo Negocio",
    "email_notificacion": "negocio@example.com"
  }'
```

---

## Listar clientes (admin)

```bash
curl -u admin:secreto http://localhost:5500/admin/clientes
```

---

## Ver mensajes de un cliente

```bash
curl -u admin:secreto http://localhost:5500/admin/clientes/ismaelpalencia/mensajes
```

---

# Notas importantes

- El token de Turnstile en desarrollo puede ser el de prueba `1x00000000000000000000AA`.
- En producción debe usarse el token real.
- Las fechas se manejan en **formato ISO 8601**.
- Para los endpoints de admin, reemplaza `admin:secreto` con las credenciales reales.

---

**Versión:** 1.5.0  
**Última actualización:** 15 de marzo de 2025