# 🚀 FastAPI Async CRUD - Sistema de Gestión de Usuarios

API REST completamente asíncrona construida con **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, **Docker** y **Alembic** para gestión de usuarios con autenticación JWT.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120.3-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.1-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-red.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
  - [Con Docker (Recomendado)](#-opción-1-con-docker-recomendado)
  - [Sin Docker](#-opción-2-sin-docker-desarrollo-local)
- [Configuración](#-configuración)
- [Migraciones con Alembic](#-migraciones-con-alembic)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Autenticación JWT](#-autenticación-jwt)
- [Testing](#-testing)
- [Contribuir](#-contribuir)

---

## ✨ Características

- ✅ **Completamente Asíncrono** - Operaciones no bloqueantes con `asyncio`
- ✅ **Autenticación JWT** - Sistema seguro de tokens con `python-jose`
- ✅ **CRUD Completo** - Create, Read, Update, Delete de usuarios
- ✅ **Gestión de Perfil** - Los usuarios pueden gestionar su propio perfil
- ✅ **Soft Delete** - Eliminación lógica de registros
- ✅ **Validación Robusta** - Validación de contraseñas con requisitos de seguridad
- ✅ **PostgreSQL** - Base de datos relacional con `asyncpg`
- ✅ **Docker & Docker Compose** - Despliegue containerizado
- ✅ **Alembic** - Migraciones de base de datos versionadas
- ✅ **Middleware Personalizado** - Medición de tiempo de respuesta
- ✅ **Documentación Automática** - Swagger UI y ReDoc
- ✅ **Hashing Seguro** - Contraseñas hasheadas con `argon2`
- ✅ **Type Hints** - Código completamente tipado

---

## 🛠️ Tecnologías

| Tecnología      | Versión | Propósito                   |
| --------------- | ------- | --------------------------- |
| **Python**      | 3.13    | Lenguaje base               |
| **FastAPI**     | 0.120.3 | Framework web asíncrono     |
| **PostgreSQL**  | 17.1    | Base de datos               |
| **SQLAlchemy**  | 2.0.44  | ORM asíncrono               |
| **Alembic**     | 1.17.1  | Migraciones de BD           |
| **Pydantic**    | 2.12.3  | Validación de datos         |
| **asyncpg**     | 0.30.0  | Driver PostgreSQL asíncrono |
| **python-jose** | 3.5.0   | JWT tokens                  |
| **argon2-cffi** | 25.1.0  | Hashing de contraseñas      |
| **Docker**      | Latest  | Containerización            |
| **Uvicorn**     | 0.38.0  | Servidor ASGI               |

---

## 📦 Requisitos Previos

### Con Docker:

- Docker 20.10+
- Docker Compose 2.0+

### Sin Docker:

- Python 3.9+
- PostgreSQL 13+
- pip

---

## 🚀 Instalación

### 🐳 Opción 1: Con Docker (Recomendado)

#### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/fastapi-async-crud.git
cd fastapi-async-crud
```

#### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://luzardo:luzardo2004@db:5432/miapp

# JWT
SECRET_KEY=tu_clave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 3. Construir y ejecutar con Docker Compose

```bash
# Construir las imágenes
docker-compose build

# Iniciar los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app
```

#### 4. Ejecutar migraciones

```bash
# Acceder al contenedor
docker-compose exec app sh

# Ejecutar migraciones
alembic upgrade head
```

La API estará disponible en: **http://localhost:8765**

#### Comandos útiles de Docker:

```bash
# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs
docker-compose logs -f

# Eliminar volúmenes (⚠️ borra la BD)
docker-compose down -v
```

---

### 💻 Opción 2: Sin Docker (Desarrollo Local)

#### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/fastapi-async-crud.git
cd fastapi-async-crud
```

#### 2. Crear entorno virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configurar PostgreSQL

Instala PostgreSQL y crea una base de datos:

```sql
CREATE DATABASE fastapi_db;
CREATE USER postgres WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO postgres;
```

#### 5. Configurar variables de entorno

Crea un archivo `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:1234@localhost:5432/fastapi_db
SECRET_KEY=53011238
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 6. Ejecutar migraciones

```bash
# Inicializar Alembic (si no está inicializado)
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

#### 7. Ejecutar la aplicación

```bash
# Modo desarrollo
fastapi dev app/main.py --host 0.0.0.0 --port 8765

# O con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8765
```

La API estará disponible en: **http://localhost:8765**

---

## ⚙️ Configuración

### Variables de Entorno

| Variable                      | Descripción                    | Ejemplo                                       |
| ----------------------------- | ------------------------------ | --------------------------------------------- |
| `DATABASE_URL`                | URL de conexión a PostgreSQL   | `postgresql+asyncpg://user:pass@host:5432/db` |
| `SECRET_KEY`                  | Clave secreta para JWT         | `tu_clave_super_secreta`                      |
| `ALGORITHM`                   | Algoritmo de encriptación JWT  | `HS256`                                       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token | `30`                                          |

### Archivo `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🗄️ Migraciones con Alembic

### Comandos principales:

```bash
# Crear una nueva migración automática
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ver estado actual
alembic current
```

### Ejemplo de flujo de trabajo:

```bash
# 1. Modificar modelos en app/models/
# 2. Crear migración
alembic revision --autogenerate -m "Add email field to users"

# 3. Revisar el archivo generado en alembic/versions/
# 4. Aplicar migración
alembic upgrade head
```

---

## 📁 Estructura del Proyecto

```
API/
├── app/
│   ├── __pycache__/
│   ├── crud/
│   │   └── base.py              # CRUD genérico reutilizable
│   ├── models/
│   │   └── users.py             # Modelo SQLAlchemy de usuarios
│   ├── routes/
│   │   ├── auth.py              # Endpoints de autenticación
│   │   └── users.py             # Endpoints de usuarios
│   ├── schemas/
│   │   ├── tokens.py            # Schemas de JWT
│   │   └── users.py             # Schemas de usuarios
│   ├── utils/
│   │   ├── dependencies.py      # Dependencias reutilizables
│   │   └── security.py          # Funciones de seguridad
│   ├── __init__.py
│   ├── config.py                # Configuración de la app
│   ├── database.py              # Configuración de BD
│   ├── main.py                  # Punto de entrada
│   └── middleware.py            # Middlewares personalizados
├── alembic/
│   ├── versions/                # Migraciones
│   └── env.py
├── test/
│   └── __init__.py
├── .dockerignore
├── .env                         # Variables de entorno
├── .gitignore
├── alembic.ini                  # Configuración de Alembic
├── docker-compose.yml           # Orquestación de contenedores
├── Dockerfile                   # Imagen de Docker
├── README.md                    # Este archivo
└── requirements.txt             # Dependencias Python
```

---

## 🔌 Endpoints de la API

### 📚 Documentación Interactiva

- **Swagger UI**: http://localhost:8765/docs
- **ReDoc**: http://localhost:8765/redoc

### Autenticación

| Método | Endpoint         | Descripción             | Autenticación |
| ------ | ---------------- | ----------------------- | ------------- |
| POST   | `/auth/register` | Registrar nuevo usuario | No            |
| POST   | `/auth/login`    | Iniciar sesión (JSON)   | No            |
| POST   | `/auth/token`    | Obtener token (Form)    | No            |

### Usuarios

| Método | Endpoint            | Descripción                       | Autenticación |
| ------ | ------------------- | --------------------------------- | ------------- |
| GET    | `/user/all`         | Obtener todos los usuarios        | Sí            |
| GET    | `/user/me`          | Obtener perfil del usuario actual | Sí            |
| GET    | `/user/{id}`        | Obtener usuario por ID            | Sí            |
| POST   | `/user/create`      | Crear nuevo usuario               | No            |
| PUT    | `/user/update/{id}` | Actualizar usuario                | No            |
| DELETE | `/user/delete/{id}` | Eliminar usuario (soft delete)    | No            |

### General

| Método | Endpoint    | Descripción               |
| ------ | ----------- | ------------------------- |
| GET    | `/`         | Mensaje de bienvenida     |
| GET    | `/security` | Ruta protegida de ejemplo |

---

## 📝 Ejemplos de Uso

### 1. Registrar un nuevo usuario

```bash
curl -X POST "http://localhost:8765/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "mail": "john@example.com",
    "password": "MySecure123!@#"
  }'
```

**Respuesta:**

```json
{
  "id": 1,
  "username": "johndoe",
  "mail": "john@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

**Requisitos de contraseña:**

- Mínimo 10 caracteres
- Al menos un número
- Al menos una letra mayúscula
- Al menos un carácter especial (!@#$%^&\*()\_+-=[]{|};:,.<>?)

### 2. Iniciar sesión

```bash
curl -X POST "http://localhost:8765/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "MySecure123!@#"
  }'
```

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Obtener token (OAuth2 Form)

```bash
curl -X POST "http://localhost:8765/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=MySecure123!@#"
```

### 4. Obtener mi perfil

```bash
curl -X GET "http://localhost:8765/user/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Respuesta:**

```json
{
  "id": 1,
  "username": "johndoe",
  "mail": "john@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

### 5. Obtener todos los usuarios

```bash
curl -X GET "http://localhost:8765/user/all" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 6. Actualizar usuario

```bash
curl -X PUT "http://localhost:8765/user/update/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "username": "johndoe_updated",
    "mail": "newemail@example.com"
  }'
```

### 7. Eliminar usuario (Soft Delete)

```bash
curl -X DELETE "http://localhost:8765/user/delete/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 🔐 Autenticación JWT

### Flujo de autenticación:

1. **Registro/Login** → Obtener token JWT
2. **Incluir token** en el header `Authorization: Bearer <token>`
3. **Acceder** a rutas protegidas

### Estructura del JWT Payload:

```json
{
  "sub": "1",
  "username": "johndoe",
  "iat": 1705315800,
  "exp": 1705317600
}
```

### Ejemplo con Python (httpx):

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Login
        response = await client.post(
            "http://localhost:8765/auth/login",
            json={
                "username": "johndoe",
                "password": "MySecure123!@#"
            }
        )
        token = response.json()["access_token"]

        # 2. Usar token
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(
            "http://localhost:8765/user/me",
            headers=headers
        )
        print(response.json())

asyncio.run(main())
```

### Ejemplo con JavaScript (Fetch):

```javascript
// 1. Login
const loginResponse = await fetch("http://localhost:8765/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "johndoe",
    password: "MySecure123!@#",
  }),
});

const { access_token } = await loginResponse.json();

// 2. Usar token
const profileResponse = await fetch("http://localhost:8765/user/me", {
  headers: { Authorization: `Bearer ${access_token}` },
});

const profile = await profileResponse.json();
console.log(profile);
```

---

## 🧪 Testing

### Instalar dependencias de testing:

```bash
pip install pytest pytest-asyncio httpx
```

### Crear `test/test_auth.py`:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "mail": "test@example.com",
                "password": "TestPass123!@#"
            }
        )
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/auth/login",
            json={
                "username": "testuser",
                "password": "TestPass123!@#"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
```

### Ejecutar tests:

```bash
pytest
```

---

## 🐛 Troubleshooting

### Error: "Could not connect to database"

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart
```

### Error: "Alembic migration failed"

```bash
# Verificar estado de migraciones
alembic current

# Revertir y volver a aplicar
alembic downgrade -1
alembic upgrade head
```

### Error: "Port 8765 already in use"

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8766:8765"
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

### Guía de estilo:

- Usa **type hints** en todas las funciones
- Sigue **PEP 8**
- Documenta con **docstrings**
- Escribe **tests** para nuevas características

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Tu Nombre**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@example.com

---

## 🙏 Agradecimientos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## 🔜 Roadmap

- [ ] Sistema de roles y permisos (Admin, User)
- [ ] Refresh tokens
- [ ] Rate limiting
- [ ] Paginación avanzada
- [ ] Filtros y búsqueda
- [ ] Upload de imágenes de perfil
- [ ] Verificación de email
- [ ] Recuperación de contraseña
- [ ] Logging con Sentry
- [ ] Tests de integración completos
- [ ] CI/CD con GitHub Actions
- [ ] Kubernetes deployment

---

⭐ **Si este proyecto te fue útil, considera darle una estrella en GitHub!**

**Hecho con ❤️ usando FastAPI**
