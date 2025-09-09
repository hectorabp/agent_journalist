from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el módulo
sys.path.append(str(Path(__file__).resolve().parent.parent))
from modules.categories import Categories

categories_controller = Categories()
categories_blueprint = Blueprint("categories_routes", __name__)

# --- HANDLERS ---
def create_category_handler():
    try:
        data = request.get_json() or {}
        nombre = data.get("categoria")
        if not nombre:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'categoria'. Formato esperado: { 'categoria': str }"
            }), 400
        result = categories_controller.create({"categoria": nombre})
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def read_category_handler():
    try:
        categoria_id = request.args.get("categoria_id")
        if not categoria_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'categoria_id'. Formato esperado: /categories/read?categoria_id=ID"
            }), 400
        result = categories_controller.get_by_id(categoria_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def get_all_categories_handler():
    try:
        result = categories_controller.get_all()
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def update_category_handler():
    try:
        data = request.get_json() or {}
        categoria_id = data.get("categoria_id")
        nombre = data.get("categoria")
        if not categoria_id or not nombre:
            return jsonify({
                "status": False,
                "message": "Faltan variables obligatorias: 'categoria_id', 'categoria'. Formato esperado: { 'categoria_id': int, 'categoria': str }"
            }), 400
        result = categories_controller.update(categoria_id, {"categoria": nombre})
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def delete_category_handler():
    try:
        data = request.get_json() or {}
        categoria_id = data.get("categoria_id")
        if not categoria_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'categoria_id'. Formato esperado: { 'categoria_id': int }"
            }), 400
        result = categories_controller.delete(categoria_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

# --- RUTAS ---
categories_blueprint.add_url_rule(
    "/categories/create",
    view_func=create_category_handler,
    methods=["POST"]
)
categories_blueprint.add_url_rule(
    "/categories/read",
    view_func=read_category_handler,
    methods=["GET"]
)
categories_blueprint.add_url_rule(
    "/categories/all",
    view_func=get_all_categories_handler,
    methods=["GET"]
)
categories_blueprint.add_url_rule(
    "/categories/update",
    view_func=update_category_handler,
    methods=["PUT"]
)
categories_blueprint.add_url_rule(
    "/categories/delete",
    view_func=delete_category_handler,
    methods=["DELETE"]
)
