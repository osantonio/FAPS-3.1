# Sistema de Gestión de Entregas FAPS

Este sistema es una aplicación web desarrollada con Flask para la gestión de entregas, residentes y suministros. Está diseñado para facilitar el control y seguimiento de entregas en un entorno administrativo.

## Características Principales

- **Gestión de Usuarios**: Sistema completo de autenticación y autorización
- **Gestión de Residentes**: Registro y administración de información de residentes
- **Control de Suministros**: Inventario y gestión de suministros disponibles
- **Sistema de Entregas**: Registro y seguimiento de entregas a residentes
- **Interfaz Administrativa**: Panel de control intuitivo para todas las operaciones
- **Seguridad**: Implementación robusta de medidas de seguridad
- **Procesamiento Asíncrono**: Manejo de tareas en segundo plano con Celery

## Estructura del Proyecto

```
FAPS-3/
├── app/
│   ├── routes/
│   │   ├── delivery_routes.py
│   │   ├── resident_routes.py
│   │   ├── supply_routes.py
│   │   └── user_routes.py
│   ├── templates/
│   ├── models.py
│   └── extensions.py
├── migrations/
├── celery.py
├── config.py
└── main.py
```

## Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL
- Redis (para Celery y caché)

## Configuración del Entorno

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd FAPS-3
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Unix/MacOS:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```bash
   # Crea un archivo .env con las siguientes variables
   FLASK_APP=main.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://[usuario]:[contraseña]@localhost/faps
   SECRET_KEY=[tu_clave_secreta]
   REDIS_URL=redis://localhost:6379/0
   ```

5. Inicializa la base de datos:
   ```bash
   flask db upgrade
   ```

## Ejecución del Proyecto

1. Inicia Redis:
   ```bash
   redis-server
   ```

2. Inicia Celery (en una terminal separada):
   ```bash
   celery -A celery.celery worker --loglevel=info
   ```

3. Inicia la aplicación Flask:
   ```bash
   flask run
   ```

## Funcionalidades Implementadas

### Módulo de Usuarios
- Registro y autenticación de usuarios
- Gestión de roles y permisos
- Panel de administración de usuarios

### Módulo de Residentes
- Registro completo de información de residentes
- Historial de entregas por residente
- Búsqueda y filtrado de residentes

### Módulo de Suministros
- Inventario detallado de suministros
- Control de stock
- Historial de movimientos

### Módulo de Entregas
- Registro de entregas
- Seguimiento de estado
- Reportes y estadísticas

## Seguridad

- Autenticación mediante Flask-Login
- Protección CSRF
- Encriptación de contraseñas con Bcrypt
- Headers de seguridad con Flask-Talisman

## Mantenimiento

Para mantener el sistema actualizado:

1. Actualiza las dependencias regularmente
2. Ejecuta las migraciones pendientes
3. Revisa los logs de errores
4. Realiza backups de la base de datos

## Soporte

Para reportar problemas o solicitar nuevas características, por favor crear un issue en el repositorio. 