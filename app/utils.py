import os
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads/profile_photos'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_photo(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    if file and allowed_file(file.filename):
        # Generar un nombre único para el archivo
        filename = secure_filename(file.filename)
        unique_filename = f"{str(uuid.uuid4())}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Guardar el archivo
        file.save(file_path)
        
        # Devolver la ruta relativa para guardar en la base de datos
        return f"uploads/profile_photos/{unique_filename}"
    
    return None 