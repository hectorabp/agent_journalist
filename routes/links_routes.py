from flask import Blueprint, request, jsonify
import datetime
import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.links import Links

links_controller = Links()
links_blueprint = Blueprint("links_routes", __name__)

# --- HANDLERS ---

def create_link_handler():
    try:
        now = datetime.datetime.now()
        data = request.get_json() or {}
        medio = data.get("medio")
        titulo = data.get("titulo")
        link = data.get("link")
        nota = data.get("nota")
        if not medio or not titulo or not link or nota is None:
            return jsonify({
                "status": False,
                "message": "Faltan variables obligatorias: 'medio', 'titulo', 'link', 'nota'. Formato esperado: { 'medio': str, 'titulo': str, 'link': str, 'fecha': str, 'nota': str }"
            }), 400
        result = links_controller.create({
            'medio': medio,
            'titulo': titulo,
            'link': link,
            'fecha': now,
            'nota': nota
        })
        return jsonify({"status": True, "result": result})
    except Exception as e:
        print(f"[ERROR_CREATE_LINK]: {e}")
        return jsonify({"status": False, "message": str(e)}), 500

def read_link_handler():
    try:
        link_id = request.args.get("link_id")
        if not link_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'link_id'. Formato esperado: /links/read?link_id=ID"
            }), 400
        result = links_controller.get_by_id(link_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def get_all_links_handler():
    try:
        result = links_controller.get_all()
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
        result = links_controller.update(link_id, update_data)
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
        result = links_controller.delete(link_id)
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
