# Agente Periodista

Microservicio Flask para gestionar links periodísticos y notas (archivos TXT).

## Contenido del repositorio
- `app.py` - Punto de entrada de la aplicación Flask.
- `routes/`, `templates/`, `static/` - Vistas, plantillas y recursos estáticos.
- `modules/` - Módulos de acceso a datos y utilidades (DB, CRUD, txt manager).
- `notas/` - Carpeta con archivos .txt generados.
- `docker-compose.yml` - Compose para desplegar localmente (servicio `agent_dashboard`, `db_agent`, `phpmyadmin`).

## Requisitos
- Docker y Docker Compose en la máquina (VPS).
- MySQL o usar el servicio `db_agent` incluido.

## Despliegue local / VPS
1. Copia este repositorio al VPS.
2. Ajusta las variables de entorno si es necesario (por ejemplo, contraseñas en `docker-compose.yml`).
3. Levanta los servicios:

```powershell
# en la carpeta del proyecto
docker compose up -d --build
```

4. Si en el VPS usas Traefik para enrutamiento, ya incluimos labels en `docker-compose.yml` para exponer `/agent` y `/agent/phpmyadmin`. Asegúrate de que el Traefik principal tenga:
- Un `entrypoint` llamado `web` expuesto en :80.
- `providers.docker` habilitado y `exposedbydefault=false` si quieres controlar los servicios con labels.

## Cómo inicializar el repositorio git y subir a GitHub
```powershell
git init
git add .
git commit -m "Initial commit: Agente Periodista"
#Crear el repo en GitHub/GitLab y añadir remoto
git remote add origin <URL_DEL_REPO>
git branch -M main
git push -u origin main
```

## Notas
- Ver `templates/notes.html` y `static/js/notes.js` para la lógica de filtros, carga y render de notas.
- El proyecto usa archivos `.txt` para almacenar el contenido de las notas en la carpeta `notas/`.
- Si quieres que prepare CI/CD (por ejemplo GitHub Actions para deploy), dime y lo agrego.
