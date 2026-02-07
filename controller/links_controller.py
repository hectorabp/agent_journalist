import sys
import datetime
from pathlib import Path

# Añadimos el directorio principal al path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.links import Links

class LinksController:
    """
    Controlador para gestionar la lógica de negocio de los links.
    """
    def __init__(self):
        self.links_model = Links()

    def create_links(self, data):
        """
        Inserta uno o varios links en la base de datos.
        Permite recibir un diccionario (un solo link) o una lista de diccionarios.
        
        Retorna un resumen de la operación.
        """
        # Normalizar entrada a lista
        if isinstance(data, dict):
            items = [data]
        elif isinstance(data, list):
            items = data
        else:
            return {"status": "error", "message": "Formato de datos inválido. Se espera dict o list."}

        created_ids = []
        existing_links = []
        errors = []

        for item in items:
            try:
                # Asignar fecha por defecto si no existe
                if 'fecha' not in item or not item['fecha']:
                    item['fecha'] = datetime.datetime.now()

                link_url = item.get('link')
                # Verificar si ya existe
                existing_id = self.links_model.check_existence(link_url)
                
                if existing_id:
                    existing_links.append(link_url)
                else:
                    # item debe tener keys: 'medio', 'titulo', 'link', 'fecha', 'nota', 'id_categoria'
                    new_id = self.links_model.create(item)
                    if new_id:
                        created_ids.append({"id": new_id, "link": link_url})
            except Exception as e:
                errors.append({"link": item.get('link'), "error": str(e)})

        return {
            "status": "completed",
            "created_count": len(created_ids),
            "existing_count": len(existing_links),
            "error_count": len(errors),
            "created_details": created_ids,
            "existing_details": existing_links,
            "errors": errors
        }

    def get_all_links(self):
        return self.links_model.get_all()

    def get_link_by_id(self, link_id):
        return self.links_model.get_by_id(link_id)

    def update_link(self, link_id, data):
        return self.links_model.update(link_id, data)

    def delete_link(self, link_id):
        return self.links_model.delete(link_id)
