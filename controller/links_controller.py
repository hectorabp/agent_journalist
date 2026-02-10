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
        
        Retorna un resumen de la operación agrupado por medio.
        """
        # Normalizar entrada a lista
        if isinstance(data, dict):
            items = [data]
        elif isinstance(data, list):
            items = data
        else:
            return {"status": "error", "message": "Formato de datos inválido. Se espera dict o list."}

        results_by_media = {}
        total_created = 0
        total_existing = 0
        total_errors = 0

        for item in items:
            medio = item.get('medio', 'Desconocido')
            if medio not in results_by_media:
                results_by_media[medio] = {'created': [], 'existing': [], 'errors': []}

            try:
                # Asignar fecha por defecto si no existe
                if 'fecha' not in item or not item['fecha']:
                    item['fecha'] = datetime.datetime.now()

                link_url = item.get('link')
                # Verificar si ya existe
                existing_id = self.links_model.check_existence(link_url)
                
                if existing_id:
                    results_by_media[medio]['existing'].append(link_url)
                    total_existing += 1
                else:
                    # item debe tener keys: 'medio', 'titulo', 'link', 'fecha', 'nota', 'id_categoria'
                    new_id = self.links_model.create(item)
                    if new_id:
                        results_by_media[medio]['created'].append({"id": new_id, "link": link_url})
                        total_created += 1
            except Exception as e:
                results_by_media[medio]['errors'].append({"link": item.get('link'), "error": str(e)})
                total_errors += 1

        return {
            "status": "completed",
            "summary": {
                "created_count": total_created,
                "existing_count": total_existing,
                "error_count": total_errors
            },
            "details_by_media": results_by_media
        }

    def get_all_links(self):
        return self.links_model.get_all()

    def get_link_by_id(self, link_id):
        return self.links_model.get_by_id(link_id)

    def update_link(self, link_id, data):
        return self.links_model.update(link_id, data)

    def delete_link(self, link_id):
        return self.links_model.delete(link_id)
