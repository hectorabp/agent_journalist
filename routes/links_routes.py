from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from controller.links_controller import LinksController

links_controller = LinksController()
links_blueprint = Blueprint("links_routes", __name__)

# --- HANDLERS ---

def create_link_handler():
    try:
        data = request.get_json() or {}
        # Llamamos al controlador que soporta uno o varios links
        result = links_controller.create_links(data)
        return jsonify(result)
    except Exception as e:
        print(f"[ERROR_CREATE_LINK]: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def read_link_handler():
    try:
        link_id = request.args.get("link_id")
        if not link_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'link_id'. Formato esperado: /links/read?link_id=ID"
            }), 400
        result = links_controller.get_link_by_id(link_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def get_all_links_handler():
    try:
        result = links_controller.get_all_links()
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def update_link_handler():
    try:
        data = request.get_json() or {}
        link_id = data.get("link_id")
        update_data = data.get("update_data")
        if not link_id or not update_data:
            return jsonify({
                "status": False,
                "message": "Faltan variables obligatorias: 'link_id', 'update_data'. Formato esperado: { 'link_id': int, 'update_data': dict }"
            }), 400
        result = links_controller.update_link(link_id, update_data)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def delete_link_handler():
    try:
        data = request.get_json() or {}
        link_id = data.get("link_id")
        if not link_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'link_id'. Formato esperado: { 'link_id': int }"
            }), 400
        result = links_controller.delete_link(link_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

# --- RUTAS ---
links_blueprint.add_url_rule(
    "/links/create",
    view_func=create_link_handler,
    methods=["POST"]
)
links_blueprint.add_url_rule(
    "/links/read",
    view_func=read_link_handler,
    methods=["GET"]
)
links_blueprint.add_url_rule(
    "/links/all",
    view_func=get_all_links_handler,
    methods=["GET"]
)
links_blueprint.add_url_rule(
    "/links/update",
    view_func=update_link_handler,
    methods=["PUT"]
)
links_blueprint.add_url_rule(
    "/links/delete",
    view_func=delete_link_handler,
    methods=["DELETE"]
)
