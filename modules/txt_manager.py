import os

NOTAS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notas')

class TxtManager:

    """
    Clase para crear, editar y eliminar archivos .txt en la carpeta notas.
    """
    def __init__(self, base_dir=NOTAS_DIR):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _get_path(self, filename):
        if not filename.endswith('.txt'):
            filename += '.txt'
        return os.path.join(self.base_dir, filename)

    def read_txt(self, filename):
        """
        Lee y retorna el contenido completo de un archivo txt.
        """
        path = self._get_path(filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {filename} no existe.")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def create_txt(self, filename, content=""):
        """
        Crea un archivo txt con el contenido dado. Si existe, lo sobrescribe.
        """
        path = self._get_path(filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def edit_txt(self, filename, content):
        """
        Edita (sobrescribe) el contenido de un archivo txt existente.
        """
        path = self._get_path(filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {filename} no existe.")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def delete_txt(self, filename):
        """
        Elimina un archivo txt.
        """
        path = self._get_path(filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            raise FileNotFoundError(f"El archivo {filename} no existe.")
