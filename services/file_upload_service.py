import os
import uuid
from werkzeug.utils import secure_filename

# Base upload folder (centralized)
BASE_UPLOAD_FOLDER = "uploads"

# Allowed file formats
DEFAULT_ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename, allowed_ext=DEFAULT_ALLOWED_EXTENSIONS):
    """
    Check if the file extension is allowed.
    """
    if not filename or "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_ext


def generate_unique_filename(filename):
    """
    Creates a unique filename using UUID to avoid collisions.
    """
    ext = filename.rsplit(".", 1)[1]
    return f"{uuid.uuid4().hex}.{ext}"


def save_file(file, folder, allowed_ext=DEFAULT_ALLOWED_EXTENSIONS, max_size_mb=5):
    """
    Saves an uploaded file safely with validations.
    
    Parameters:
        file        (FileStorage) : uploaded file
        folder      (str)         : subfolder inside uploads/
        allowed_ext (set)         : allowed extensions
        max_size_mb (int)         : max file size allowed (MB)
    
    Returns:
        str (relative file path) OR None
    """

    # No file selected
    if not file or file.filename == "":
        return None

    # Validate extension
    original_filename = secure_filename(file.filename)
    if not allowed_file(original_filename, allowed_ext):
        return None

    # Validate file size (prevents huge uploads)
    file.seek(0, os.SEEK_END)
    file_size = file.tell() / (1024 * 1024)  # MB
    file.seek(0)

    if file_size > max_size_mb:
        print(f"[UPLOAD BLOCKED] File too large: {file_size} MB")
        return None

    # Ensure upload folder exists
    upload_path = os.path.join(BASE_UPLOAD_FOLDER, folder)
    os.makedirs(upload_path, exist_ok=True)

    # Always save with a unique filename
    unique_filename = generate_unique_filename(original_filename)
    full_save_path = os.path.join(upload_path, unique_filename)

    # Save file
    file.save(full_save_path)

    # Return a clean, relative path for database usage
    relative_path = f"{BASE_UPLOAD_FOLDER}/{folder}/{unique_filename}"
    return relative_path