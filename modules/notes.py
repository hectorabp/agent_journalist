import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.config import Database

class Notes:
    """
    Clase para operaciones CRUD sobre la tabla notas.
    """
    def __init__(self):
        self.db = Database()

    def create(self, data):
        """
        Inserta un nuevo registro en la tabla notas.
        data: dict con las claves 'titulo', 'nombre_archivo', 'id_categoria', 'ultima_modificacion', 'id_link' (opcional)
        Retorna el id insertado.
        """
        query = """
            INSERT INTO notas (titulo, nombre_archivo, id_categoria, id_link, ultima_modificacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('titulo'),
            data.get('nombre_archivo'),
            data.get('id_categoria'),
            data.get('id_link'),
            data.get('ultima_modificacion')
        )
        return self.db.insert_query(query, params)

    def get_by_id(self, nota_id):
        """
        Obtiene un registro de notas por su id.
        """
        query = "SELECT * FROM notas WHERE id = %s"
        result = self.db.query(query, (nota_id,))
        return result[0] if result else None

    def get_all(self):
        """
        Obtiene todos los registros de la tabla notas.
        """
        query = "SELECT * FROM notas"
        return self.db.query(query)

    def update(self, nota_id, data):
        """
        Actualiza un registro de notas por su id.
        data: dict con las claves a actualizar.
        """
        fields = []
        params = []
        for key in ['titulo', 'nombre_archivo', 'id_categoria', 'id_link', 'ultima_modificacion']:
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(nota_id)
        query = f"UPDATE notas SET {', '.join(fields)} WHERE id = %s"
        self.db.query(query, tuple(params))
        return True

    def delete(self, nota_id):
        """
        Elimina un registro de notas por su id.
        """
        query = "DELETE FROM notas WHERE id = %s"
        self.db.query(query, (nota_id,))
        return True
