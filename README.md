# Proyecto Flask

Este proyecto es una aplicación web construida con Flask que utiliza varias extensiones para proporcionar funcionalidades como autenticación, seguridad, caché y más.

## Estructura del Proyecto

- **app/**: Contiene la lógica principal de la aplicación.
  - **\_\_init\_\_.py**: Configura la aplicación Flask y sus extensiones.
  - **models.py**: Define los modelos de base de datos utilizando SQLAlchemy.
  - **routes.py**: Define las rutas de la aplicación.
- **config.py**: Archivo de configuración para la aplicación.
- **main.py**: Punto de entrada principal de la aplicación.
- **celery.py**: Configuración para tareas asíncronas con Celery.
- **static/**: Archivos estáticos como CSS y JavaScript.
- **templates/**: Plantillas HTML para la aplicación.
- **requirements.txt**: Lista de dependencias del proyecto.

## Funcionalidades

- **Autenticación y Seguridad**: Utiliza Flask-Security para manejar la autenticación de usuarios y roles.
- **Caché**: Implementado con Flask-Caching para mejorar el rendimiento.
- **Protección**: Flask-Talisman se utiliza para mejorar la seguridad de la aplicación.

## Rutas del Sistema

### Rutas de Usuarios
- **GET/POST** `/admin/users/create` - Crear nuevo usuario
- **GET** `/admin/users` - Listar todos los usuarios
- **GET/POST** `/admin/users/edit/<id>` - Editar usuario específico
- **POST** `/admin/users/delete/<id>` - Eliminar usuario específico

### Rutas de Residentes
- **GET/POST** `/admin/residents/create` - Crear nuevo residente
- **GET** `/admin/residents` - Listar todos los residentes
- **GET/POST** `/admin/residents/edit/<id>` - Editar residente específico
- **POST** `/admin/residents/delete/<id>` - Eliminar residente específico

### Rutas de Suministros
- **GET/POST** `/admin/supplies/create` - Crear nuevo suministro
- **GET** `/admin/supplies` - Listar todos los suministros
- **GET/POST** `/admin/supplies/edit/<id>` - Editar suministro específico
- **POST** `/admin/supplies/delete/<id>` - Eliminar suministro específico

### Rutas de Entregas
- **GET/POST** `/admin/deliveries/create` - Crear nueva entrega
- **GET** `/admin/deliveries` - Listar todas las entregas
- **GET/POST** `/admin/deliveries/edit/<id>` - Editar entrega específica
- **POST** `/admin/deliveries/delete/<id>` - Eliminar entrega específica

## Requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login
- Flask-Caching
- Flask-Security
- Flask-Talisman
- Celery

## Instalación

1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv .venv`
3. Activa el entorno virtual: 
   - En Windows: `.venv\Scripts\activate`
   - En Unix o MacOS: `source .venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`

## Ejecución

1. Configura las variables de entorno necesarias.
2. Inicia la aplicación: `python main.py`

## Mejoras Necesarias

- **Implementación de Funcionalidades CRUD**: Asegúrate de que todas las operaciones CRUD estén implementadas para los modelos.
- **Pruebas**: Añadir pruebas unitarias para asegurar la calidad del código.
- **Documentación**: Completar la documentación de la API y del código.
- **Despliegue**: Configurar un entorno de despliegue para producción. 