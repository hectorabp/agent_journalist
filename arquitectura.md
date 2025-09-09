
# arquitectura.md
#
## Estructura de la base de datos

La base de datos `agent` contiene las siguientes tablas principales:

### Tabla `categorias`
| Campo      | Tipo           | Descripción                |
|------------|----------------|----------------------------|
| id         | int, PK, AI    | Identificador único        |
| categoria  | varchar(255)   | Nombre de la categoría     |

### Tabla `links`
| Campo   | Tipo           | Descripción                                 |
|---------|----------------|---------------------------------------------|
| id      | int, PK, AI    | Identificador único                        |
| medio   | varchar(255)   | Medio periodístico                         |
| titulo  | varchar(255)   | Título de la noticia                       |
| link    | varchar(255)   | URL de la noticia                          |
| fecha   | datetime       | Fecha de registro                          |
| nota    | varchar(5)     | Indica si tiene nota asociada ('Si'/'No')  |

### Tabla `notas`
| Campo               | Tipo           | Descripción                          |
|---------------------|----------------|--------------------------------------|
| id                  | int, PK, AI    | Identificador único                  |
| titulo              | varchar(255)   | Título de la nota                    |
| nombre_archivo      | varchar(255)   | Nombre del archivo .txt asociado     |
| id_categoria        | int            | Relación con la tabla categorias     |
| id_link             | int, NULL      | Relación con la tabla links (opcional)|
| ultima_modificacion | datetime       | Fecha/hora de última edición        |

Notas:
- Todas las tablas usan `id` como clave primaria autoincremental.
- Los archivos `.txt` de las notas se almacenan en la carpeta `notas/` y su nombre se guarda en `nombre_archivo`.


## Descripción general del sistema
Este sistema es un microservicio Flask para la gestión de links periodísticos y notas asociadas, permitiendo registrar, editar, eliminar y consultar tanto los links como las notas desarrolladas (archivos txt) y su relación. El sistema también gestiona categorías y permite la administración de archivos txt físicos en el servidor.

## Estructura de carpetas y archivos principales

- `app.py`: Punto de entrada principal de la aplicación Flask. Registra los blueprints de rutas y arranca el servidor.
- `controller/notes_txt_controller.py`: Controlador principal para la gestión de notas y archivos txt, orquestando la lógica entre base de datos y archivos físicos.
- `modules/`: Contiene los módulos de acceso a datos y utilidades:
  - `config.py`: Clase `Database` para la conexión y operaciones con MySQL.
  - `links.py`: Clase `Links` para CRUD sobre la tabla `links`.
  - `notas_crud.py` y `notes.py`: Clases para CRUD sobre la tabla `notas`.
  - `categorias_crud.py`: Clase para CRUD sobre la tabla `categorias`.
  - `txt_manager.py`: Clase para crear, leer, editar y eliminar archivos `.txt` en la carpeta `notas`.
- `notas/`: Carpeta donde se almacenan los archivos `.txt` de las notas desarrolladas.
- `static/`: Archivos estáticos para la interfaz web.
  - `css/style.css`: Estilos personalizados.
  - `js/app.js`: Funciones AJAX reutilizables.
  - `js/links.js`: Lógica JS para la vista de links.
  - `js/notes.js`: Lógica JS para la vista de notas.
- `templates/`: Plantillas HTML Jinja para la interfaz web.
  - `base.html`: Plantilla base para todas las vistas.
  - `index.html`, `links.html`, `notes.html`: Vistas principales que heredan de base.html.
- `routes/`: Carpeta con las rutas Flask (blueprints) para exponer la API y vistas web:
  - `links_routes.py`: Rutas para CRUD de links.
  - `notes_txt_routes.py`: Rutas para CRUD de notas y archivos txt.
  - `web_routes.py`: Rutas para renderizar las vistas web (index, links, notes).

## Controlador principal: `NotesTxtController` (`controller/notes_txt_controller.py`)
Este controlador centraliza la lógica de gestión de notas y archivos txt. Sus métodos principales son:


- `create_note(titulo, id_categoria, content, link_id=None)`: Crea un registro en la tabla `notas`, genera el archivo `.txt` correspondiente y, si se provee `link_id`, lo guarda en la columna `id_link` y actualiza el campo `nota` del link a "Si".
- `read_note(nota_id)`: Devuelve los datos de la nota (incluyendo `id_link`) y el contenido del archivo `.txt` asociado.
- `edit_note(nota_id, new_content, new_titulo=None, new_id_categoria=None, new_id_link=None)`: Edita el registro y el archivo `.txt` de la nota. Permite cambiar la categoría, el título y el link asociado (`id_link`). Si cambia la categoría, renombra el archivo siguiendo la política de nombres.
- `delete_note(nota_id)`: Elimina el registro de la nota y el archivo `.txt` asociado.

Todos los métodos están envueltos en bloques try-except para registrar y propagar errores correctamente.

## Módulos principales (`modules/`)

- `config.py`: Clase `Database` para conexión y operaciones SQL con MySQL.
- `links.py`: Clase `Links` para CRUD sobre la tabla `links` (campos: medio, titulo, link, fecha, nota).
- `notes.py`: Clase `Notes` para CRUD sobre la tabla `notas` (campos: titulo, nombre_archivo, id_categoria, id_link, ultima_modificacion).
- `categorias_crud.py`: Clase para CRUD sobre la tabla `categorias` (campo: categorias).
- `txt_manager.py`: Clase para crear, leer, editar y eliminar archivos `.txt` en la carpeta `notas`.

## Rutas principales (`routes/`)

- `links_routes.py`:
  - POST `/links/create`: Crea un link. Requiere: medio, titulo, link, fecha, nota.
  - GET `/links/read?link_id=ID`: Obtiene un link por id.
  - GET `/links/all`: Lista todos los links.
  - PUT `/links/update`: Actualiza un link. Requiere: link_id, update_data (dict con campos a actualizar).
  - DELETE `/links/delete`: Elimina un link. Requiere: link_id.

- `notes_txt_routes.py`:
  - POST `/notes/create`: Crea una nota y su archivo txt. Requiere: titulo, id_categoria. Opcional: content, link_id (asociación con links).
  - GET `/notes/read?nota_id=ID`: Obtiene una nota y su archivo txt por id (incluye id_link si está asociado).
  - PUT `/notes/edit`: Edita una nota y su archivo txt. Requiere: nota_id, new_content. Opcional: new_titulo, new_id_categoria, new_id_link.
  - DELETE `/notes/delete`: Elimina una nota y su archivo txt. Requiere: nota_id.
  
- `categories_routes.py`:
  - POST `/categories/create`: Crea una categoría. Requiere: categorias.
  - GET `/categories/read?categoria_id=ID`: Obtiene una categoría por id.
  - GET `/categories/all`: Lista todas las categorías.
  - PUT `/categories/update`: Actualiza una categoría. Requiere: categoria_id, categorias.
  - DELETE `/categories/delete`: Elimina una categoría. Requiere: categoria_id.

## Dependencias
- `mysql-connector-python`: Para conexión y operaciones con MySQL.
- `python-dotenv`: Para gestión de variables de entorno.
- `Flask`: Framework web para exponer la API REST.

## Notas adicionales
- Los archivos `.txt` de las notas se almacenan en la carpeta `notas/` y su nombre sigue la convención: `id_categoria-fecha-hora-actual.txt`.
- El sistema está preparado para ser extendido con más módulos y controladores según necesidades futuras.

---
Actualizado al 31/07/2025.
