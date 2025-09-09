import datetime
import os
import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.notes import Notes
from modules.links import Links
from modules.txt_manager import TxtManager

class NotesTxtController:


    """
    Controlador para gestionar archivos txt y su registro en la base de datos.
    """
    def __init__(self):
        self.notes = Notes()
        self.txt_manager = TxtManager()
        self.links = Links()  # Importar la clase Links para manejar los links

    def _generate_filename(self, id_categoria):
        now = datetime.datetime.now()
        fecha_hora = now.strftime('%Y%m%d-%H%M%S')
        return f"{id_categoria}-{fecha_hora}.txt"


    def create_note(self, titulo, id_categoria, content, link_id=None):
        """
        Crea un registro en la tabla notas y el archivo txt correspondiente.
        Si se provee link_id, actualiza la columna 'nota' de ese link a 'Si' y lo guarda en id_link.
        Retorna el id de la nota y el nombre del archivo.
        """
        try:
            filename = self._generate_filename(id_categoria)
            data = {
                'titulo': titulo,
                'nombre_archivo': filename,
                'id_categoria': id_categoria,
                'ultima_modificacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'id_link': link_id if link_id else None
            }
            nota_id = self.notes.create(data)
            self.txt_manager.create_txt(filename, content)
            if link_id is not None:
                self.links.update(link_id, {'nota': 'Si'})
            return nota_id, filename
        except Exception as e:
            print(f"[ERROR_CREATE_NOTE]: {e}")
            raise

    def read_note(self, nota_id):
        """
        Retorna los datos de la nota y el contenido del archivo txt asociado.
        """
        try:
            nota = self.notes.get_by_id(nota_id)
            if not nota:
                raise ValueError("Nota no encontrada")
            filename = nota['nombre_archivo']
            content = self.txt_manager.read_txt(filename)
            return {**nota, 'contenido_txt': content}
        except Exception as e:
            print(f"[ERROR_READ_NOTE]: {e}")
            raise

    def edit_note(self, nota_id, new_content, new_titulo=None, new_id_categoria=None, new_id_link=None):
        """
        Edita el registro de la nota y el archivo txt correspondiente.
        Si cambia la categoría, renombra el archivo siguiendo la política.
        Permite actualizar el link asociado.
        """
        try:
            nota = self.notes.get_by_id(nota_id)
            if not nota:
                raise ValueError("Nota no encontrada")
            filename = nota['nombre_archivo']
            id_categoria = new_id_categoria if new_id_categoria else nota['id_categoria']
            # Si cambia la categoría, renombrar el archivo
            if new_id_categoria and new_id_categoria != nota['id_categoria']:
                new_filename = self._generate_filename(new_id_categoria)
                old_path = self.txt_manager._get_path(filename)
                new_path = self.txt_manager._get_path(new_filename)
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                filename = new_filename
            # Editar el archivo
            self.txt_manager.edit_txt(filename, new_content)
            # Actualizar registro en la base de datos
            update_data = {
                'nombre_archivo': filename,
                'ultima_modificacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            if new_titulo:
                update_data['titulo'] = new_titulo
            if new_id_categoria:
                update_data['id_categoria'] = new_id_categoria
            if new_id_link is not None:
                update_data['id_link'] = new_id_link
            self.notes.update(nota_id, update_data)
            return filename
        except Exception as e:
            print(f"[ERROR_EDIT_NOTE]: {e}")
            raise

    def delete_note(self, nota_id):
        """
        Elimina el registro de la nota y el archivo txt correspondiente.
        """
        try:
            nota = self.notes.get_by_id(nota_id)
            if not nota:
                raise ValueError("Nota no encontrada")
            filename = nota['nombre_archivo']
            self.txt_manager.delete_txt(filename)
            self.notes.delete(nota_id)
            return True
        except Exception as e:
            print(f"[ERROR_DELETE_NOTE]: {e}")
            raise
    def get_all_notes(self):
        """
        Retorna todas las notas desde la base de datos.
        """
        try:
            return self.notes.get_all()
        except Exception as e:
            print(f"[ERROR_GET_ALL_NOTES]: {e}")
            raise