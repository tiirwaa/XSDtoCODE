import os

def create_directory_if_not_exists(directory):
    """
    Crea un directorio si no existe.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_to_file(file_path, content):
    """
    Escribe contenido a un archivo en la ubicación dada.
    Crea las carpetas necesarias si no existen.
    """
    dir_name = os.path.dirname(file_path)
    create_directory_if_not_exists(dir_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_from_file(file_path):
    """
    Lee el contenido de un archivo dado.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
