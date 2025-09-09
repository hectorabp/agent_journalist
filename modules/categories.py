import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.config import Database

class Categories:
    """
    Clase para operaciones CRUD sobre la tabla categorias.
    """
    def __init__(self):
        self.db = Database()

    def create(self, data):
        """
        Inserta un nuevo registro en la tabla categorias.
        data: dict con la clave 'categorias'
        Retorna el id insertado.
        """
        query = """
            INSERT INTO categorias (categoria)
            VALUES (%s)
        """
        params = (data.get('categoria'),)
        return self.db.insert_query(query, params)

    def get_by_id(self, categoria_id):
        """
        Obtiene un registro de categorias por su id.
        """
        query = "SELECT * FROM categorias WHERE id = %s"
        result = self.db.query(query, (categoria_id,))
        return result[0] if result else None

    def get_all(self):
        """
        Obtiene todos los registros de la tabla categorias.
        """
        query = "SELECT * FROM categorias"
        return self.db.query(query)

    def update(self, categoria_id, data):
        """
        Actualiza un registro de categorias por su id.
        data: dict con la clave 'categorias'.
        """
        if 'categoria' not in data:
            return False
        query = "UPDATE categorias SET categoria = %s WHERE id = %s"
        params = (data['categoria'], categoria_id)
        self.db.query(query, params)
        return True

    def delete(self, categoria_id):
        """
        Elimina un registro de categorias por su id.
        """
        query = "DELETE FROM categorias WHERE id = %s"
        self.db.query(query, (categoria_id,))
        return True
