# API de Autenticación de Usuarios con FastAPI y SQLAlchemy

## Descripción

Este proyecto es una API RESTful básica para la gestión de usuarios, enfocada en las funcionalidades de autenticación: registro, inicio y cierre de sesión. Está construida con FastAPI como framework web, SQLAlchemy como ORM para la interacción con la base de datos, y MySQL como sistema de gestión de bases de datos. La seguridad de las contraseñas se maneja mediante hashing con bcrypt y la autenticación de sesiones se realiza a través de JSON Web Tokens (JWT).

## Características

- **Registro de Usuarios** (`/signup`): Permite a nuevos usuarios crear una cuenta con nombre de usuario, correo electrónico y contraseña.
- **Inicio de Sesión** (`/token`): Autentica a los usuarios y genera un JWT para futuras solicitudes.
- **Cierre de Sesión** (`/signout`): Invalida el token JWT en el cliente (la API es stateless).
- **Protección de Rutas**: Las rutas sensibles (como `/users/me/`) requieren un token JWT válido para acceder.
- **Hashing de Contraseñas**: Almacenamiento seguro de contraseñas mediante bcrypt.
- **Base de Datos MySQL**: Configurada para usar MySQL de forma asíncrona.
- **Validación de Datos**: Uso de Pydantic para la validación de entrada y salida de datos.
- **Documentación Interactiva**: FastAPI genera automáticamente documentación OpenAPI (Swagger UI) y ReDoc.

## Tecnologías Utilizadas

- **Python 3.10.6+**
- **FastAPI**: Framework web asíncrono de alto rendimiento
- **SQLAlchemy**: ORM para la interacción con la base de datos
  - `sqlalchemy[asyncio]` para operaciones asíncronas
- **MySQL**: Sistema de gestión de bases de datos relacionales
- **aiomysql**: Driver asíncrono para MySQL
- **passlib[bcrypt]**: Para el hashing seguro de contraseñas
- **python-jose[cryptography]**: Para la creación y verificación de JWT
- **python-dotenv**: Para la gestión de variables de entorno
- **uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI
- **email-validator**: Para la validación de formatos de correo electrónico
- **python-multipart**: Para el parseo de datos de formularios

## Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10.6 o superior
- MySQL Server (y acceso a un usuario, por ejemplo root con contraseña vacía)
- Puedes gestionarlo con HeidiSQL o MySQL Workbench

## Configuración e Instalación Local

Sigue estos pasos para poner en marcha la API en tu máquina local:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio # Asegúrate de estar en la raíz del proyecto
```

### 2. Crear y Activar un Entorno Virtual

Es una buena práctica aislar las dependencias de tu proyecto.

```bash
python -m venv venv

# En Windows:
.\venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar las Dependencias

Con el entorno virtual activado, instala todas las librerías necesarias:

```bash
pip install fastapi uvicorn "sqlalchemy[asyncio]" "aiomysql" "python-dotenv" "passlib[bcrypt]" "python-jose[cryptography]" "pydantic[email]" "python-multipart"
```

### 4. Configurar el Archivo .env

Crea un archivo llamado `.env` en la raíz de tu proyecto con el siguiente contenido. Asegúrate de cambiar `tu_super_secreto_para_jwt_cambialo` por una cadena de caracteres única y segura.

```env
DATABASE_URL="mysql+aiomysql://root:@localhost:3306/fastapi_db"
SECRET_KEY="tu_super_secreto_para_jwt_cambialo"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crear la Base de Datos MySQL

Abre tu herramienta de gestión de MySQL (HeidiSQL, MySQL Workbench, etc.) y crea una nueva base de datos con el nombre `fastapi_db`.

### 6. Ejecutar la Aplicación

Asegúrate de que tu entorno virtual esté activado y ejecuta:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Endpoints de la API

Una vez que la aplicación esté corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Endpoints principales:

#### POST `/signup`
Registra un nuevo usuario.

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 0,
  "username": "string",
  "email": "user@example.com"
}
```

#### POST `/token`
Inicia sesión y obtiene un token JWT.

**Request Body (form-data):**
```
username=string&password=string
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### GET `/users/me/`
Obtiene la información del usuario actualmente autenticado.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Response:**
```json
{
  "id": 0,
  "username": "string",
  "email": "user@example.com"
}
```

#### POST `/signout`
Simula el cierre de sesión (invalida el token en el cliente).

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Response:**
```json
{
  "message": "Sesión cerrada. El token ya no debe usarse."
}
```

## Flujo de Autenticación

1. **Registra un nuevo usuario** usando el endpoint `/signup`
2. **Inicia sesión** con las credenciales del usuario registrado en el endpoint `/token` para obtener un `access_token`
3. **Usa el access_token** en el encabezado Authorization (formato `Bearer <access_token>`) para acceder a las rutas protegidas, como `/users/me/`

## Estructura del Proyecto

```
tu-repositorio/
├── main.py              # Archivo principal de la aplicación
├── .env                 # Variables de entorno
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación del proyecto
```

## Consideraciones de Seguridad

- Las contraseñas se almacenan hasheadas usando bcrypt
- Los tokens JWT tienen un tiempo de expiración configurable
- La API es stateless, por lo que el cierre de sesión se maneja en el cliente
- Usa HTTPS en producción para proteger las comunicaciones

## Próximos Pasos

- Implementar refresh tokens para sesiones de larga duración
- Agregar roles y permisos de usuario
- Implementar rate limiting para prevenir ataques de fuerza bruta
- Agregar logging y monitoreo
- Configurar Docker para facilitar el despliegue