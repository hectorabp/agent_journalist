import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.config import Database

class Links:
    """
    Clase para operaciones CRUD sobre la tabla links.
    """
    def __init__(self):
        self.db = Database()

    def create(self, data):
        """
        Inserta un nuevo registro en la tabla links.
        data: dict con las claves 'medio', 'titulo', 'link', 'fecha', 'nota'
        Retorna el id insertado.
        """
        query = """
            INSERT INTO links (medio, titulo, link, fecha, nota)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('medio'),
            data.get('titulo'),
            data.get('link'),
            data.get('fecha'),
            data.get('nota')
        )
        return self.db.insert_query(query, params)

    def get_by_id(self, link_id):
        """
        Obtiene un registro de links por su id.
        """
        query = "SELECT * FROM links WHERE id = %s"
        result = self.db.query(query, (link_id,))
        return result[0] if result else None

    def get_all(self):
        """
        Obtiene todos los registros de la tabla links.
        """
        query = "SELECT * FROM links"
        return self.db.query(query)

    def update(self, link_id, data):
        """
        Actualiza un registro de links por su id.
        data: dict con las claves a actualizar.
        """
        fields = []
        params = []
        for key in ['medio', 'titulo', 'link', 'fecha', 'nota']:
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(link_id)
        query = f"UPDATE links SET {', '.join(fields)} WHERE id = %s"
        self.db.query(query, tuple(params))
        return True

    def delete(self, link_id):
        """
        Elimina un registro de links por su id.
        """
        query = "DELETE FROM links WHERE id = %s"
        self.db.query(query, (link_id,))
        return True
