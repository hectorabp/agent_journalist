
from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Añadimos el directorio principal al path para poder importar el controlador
sys.path.append(str(Path(__file__).resolve().parent.parent))
from controller.notes_txt_controller import NotesTxtController

notes_txt_controller = NotesTxtController()
notes_txt_blueprint = Blueprint("notes_txt_routes", __name__)

# --- HANDLERS ---

def create_note_handler():
    try:
        data = request.get_json() or {}
        titulo = data.get("titulo")
        id_categoria = data.get("id_categoria")
        content = data.get("content", "")
        link_id = data.get("link_id")
        if not titulo or not id_categoria:
            return jsonify({
                "status": False,
                "message": "Faltan variables obligatorias: 'titulo', 'id_categoria'. Formato esperado: { 'titulo': str, 'id_categoria': int, 'content': str, 'link_id': int (opcional) }"
            }), 400
        result = notes_txt_controller.create_note(titulo, id_categoria, content, link_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def read_note_handler():
    try:
        nota_id = request.args.get("nota_id")
        if not nota_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'nota_id'. Formato esperado: /notes/read?nota_id=ID"
            }), 400
        result = notes_txt_controller.read_note(nota_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def edit_note_handler():
    try:
        data = request.get_json() or {}
        nota_id = data.get("nota_id")
        new_content = data.get("new_content")
        new_titulo = data.get("new_titulo")
        new_id_categoria = data.get("new_id_categoria")
        new_id_link = data.get("new_id_link")
        if not nota_id or new_content is None:
            return jsonify({
                "status": False,
                "message": "Faltan variables obligatorias: 'nota_id', 'new_content'. Formato esperado: { 'nota_id': int, 'new_content': str, 'new_titulo': str (opcional), 'new_id_categoria': int (opcional), 'new_id_link': int (opcional) }"
            }), 400
        result = notes_txt_controller.edit_note(nota_id, new_content, new_titulo, new_id_categoria, new_id_link)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def delete_note_handler():
    try:
        data = request.get_json() or {}
        nota_id = data.get("nota_id")
        if not nota_id:
            return jsonify({
                "status": False,
                "message": "Falta variable obligatoria: 'nota_id'. Formato esperado: { 'nota_id': int }"
            }), 400
        result = notes_txt_controller.delete_note(nota_id)
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def get_all_notes_handler():
    try:
        result = notes_txt_controller.get_all_notes()
        return jsonify({"status": True, "result": result})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500
# --- RUTAS ---
notes_txt_blueprint.add_url_rule(
    "/notes/create",
    view_func=create_note_handler,
    methods=["POST"]
)
notes_txt_blueprint.add_url_rule(
    "/notes/read",
    view_func=read_note_handler,
    methods=["GET"]
)
notes_txt_blueprint.add_url_rule(
    "/notes/edit",
    view_func=edit_note_handler,
    methods=["PUT"]
)
notes_txt_blueprint.add_url_rule(
    "/notes/delete",
    view_func=delete_note_handler,
    methods=["DELETE"]
)
notes_txt_blueprint.add_url_rule(
    "/notes/all",
    view_func=get_all_notes_handler,
    methods=["GET"]
)