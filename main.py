from app import app
from init_app import init_database

if __name__ == "__main__":
    # Inicializar la aplicación
    init_database()
    
    # Iniciar el servidor
    app.run(debug=True, use_reloader=True)