# FAPS - Sistema de Gestión de Fundación de Adultos

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## Instalación

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd FAPS-3
```

2. Crear y activar un entorno virtual:
```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar las variables de entorno:
   - Crear un archivo `.env` en la raíz del proyecto
   - Copiar el contenido de `.env.example` y ajustar los valores

5. Inicializar la base de datos:
```bash
flask db upgrade
```

6. Crear las carpetas necesarias:
```bash
# En Windows
mkdir app\static\uploads\profile_photos
mkdir app\static\img

# En Linux/Mac
mkdir -p app/static/uploads/profile_photos app/static/img
```

7. Ejecutar la aplicación:
```bash
flask run
```

## Estructura de Directorios
```
FAPS-3/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── uploads/
│   │       └── profile_photos/
│   ├── templates/
│   ├── routes/
│   ├── models.py
│   └── utils.py
├── migrations/
├── .env
├── .gitignore
├── config.py
└── requirements.txt
```

## Configuración del Entorno

Crear un archivo `.env` con las siguientes variables:
```
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///faps.db
```

## Roles de Usuario
- **Administrador**: Acceso total al sistema
- **Colaborador**: Puede ver residentes y realizar entregas
- **Residente**: Acceso limitado a su información personal

## Notas Importantes
1. No subir al repositorio:
   - Archivos de entorno virtual (.venv)
   - Base de datos local (*.db)
   - Archivos de configuración local (.env)
   - Archivos de caché (__pycache__)
   - Archivos de medios subidos por usuarios

2. Mantener actualizadas las dependencias:
```bash
pip freeze > requirements.txt
```

3. Antes de hacer push:
   - Ejecutar las pruebas
   - Actualizar requirements.txt si se instalaron nuevas dependencias
   - No incluir archivos sensibles o personales 