// Variables globales
let allLinks = [];
let currentPage = 1;
const itemsPerPage = 10;
let filteredLinks = [];

// Cargar links por AJAX
document.addEventListener('DOMContentLoaded', function() {
    loadLinks();
    setupEventListeners();
});

// Cargar todos los links
function loadLinks() {
    ajaxRequest('GET', '/agent-journalist/links/all', null, function(status, response) {
        if(status === 200) {
            allLinks = JSON.parse(response).result;
            filteredLinks = [...allLinks];
            renderLinksTable(currentPage);
        } else {
            document.getElementById('links-table').innerHTML = '<div class="alert alert-danger">Error al cargar links.</div>';
        }
    });
}

// Configurar listeners de eventos
function setupEventListeners() {
    // Botón guardar nuevo link
    const btnSaveLink = document.getElementById('btnSaveLink');
    if (btnSaveLink) {
        btnSaveLink.addEventListener('click', saveNewLink);
    }
    
    // Botón actualizar link
    const btnUpdateLink = document.getElementById('btnUpdateLink');
    if (btnUpdateLink) {
        btnUpdateLink.addEventListener('click', updateLink);
    }
    
    // Botones de filtro
    const btnApplyFilters = document.getElementById('btnApplyFilters');
    if (btnApplyFilters) {
        btnApplyFilters.addEventListener('click', applyFilters);
    }
    
    const btnClearFilters = document.getElementById('btnClearFilters');
    if (btnClearFilters) {
        btnClearFilters.addEventListener('click', clearFilters);
    }
}

// Renderizar tabla de links con paginación
function renderLinksTable(page) {
    const tableContainer = document.getElementById('links-table');
    if (!tableContainer) return;
    
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedLinks = filteredLinks.slice(startIndex, endIndex);
    
    let html = '<table class="table table-hover"><thead><tr>';
    html += '<th>ID</th><th>Medio</th><th>Título</th><th>Link</th><th>Fecha</th><th>Nota</th><th>Acciones</th>';
    html += '</tr></thead><tbody>';
    
    if (paginatedLinks.length === 0) {
        html += '<tr><td colspan="7" class="text-center">No se encontraron links</td></tr>';
    } else {
        paginatedLinks.forEach(function(link) {
            html += `<tr>
                <td>${link.id}</td>
                <td>${link.medio}</td>
                <td>${truncateText(link.titulo, 30)}</td>
                <td><a href="${link.link}" target="_blank" class="text-truncate d-inline-block" style="max-width: 150px;">${truncateText(link.link, 25)}</a></td>
                <td>${formatDate(link.fecha)}</td>
                <td><span class="badge ${link.nota === 'Si' ? 'bg-success' : 'bg-secondary'}">${link.nota}</span></td>
                <td class="action-buttons">
                    <button class="btn btn-sm btn-outline-primary" onclick="editLink(${link.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteLink(${link.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                    ${link.nota === 'No' ? 
                        `<button class="btn btn-sm btn-outline-success" onclick="createNoteForLink(${link.id})" title="Crear nota">
                            <i class="bi bi-journal-plus"></i>
                        </button>` : 
                        `<button class="btn btn-sm btn-outline-info" onclick="viewNoteForLink(${link.id})" title="Ver nota asociada">
                            <i class="bi bi-journal-text"></i>
                        </button>`
                    }
                </td>
            </tr>`;
        });
    }
    
    html += '</tbody></table>';
    tableContainer.innerHTML = html;
    
    // Crear paginación
    createPagination(filteredLinks.length, itemsPerPage, page, 'links-pagination', function(newPage) {
        currentPage = newPage;
        renderLinksTable(currentPage);
    });
}

// Guardar nuevo link
function saveNewLink() {
    const medio = document.getElementById('medio').value.trim();
    const titulo = document.getElementById('titulo').value.trim();
    const link = document.getElementById('link').value.trim();
    const createNote = document.getElementById('createNote').checked;
    
    if (!medio || !titulo || !link) {
        showSystemMessage('Error', 'Todos los campos marcados con * son obligatorios', 'danger');
        return;
    }
    
    const data = {
        medio: medio,
        titulo: titulo,
        link: link,
        nota: createNote ? 'Si' : 'No'
    };
    
    ajaxRequest('POST', '/agent-journalist/links/create', data, function(status, response) {
        const result = JSON.parse(response);
        if (status === 200 && result.status) {
            // Cerrar modal y limpiar formulario
            const modal = bootstrap.Modal.getInstance(document.getElementById('addLinkModal'));
            modal.hide();
            document.getElementById('addLinkForm').reset();
            
            // Mostrar mensaje y recargar links
            showSystemMessage('Éxito', 'Link guardado correctamente', 'success');
            loadLinks();
            
            // Si se marcó crear nota, redirigir a la creación de nota
            if (createNote && result.result && result.result.id) {
                setTimeout(() => {
                    createNoteForLink(result.result.id);
                }, 1000);
            }
        } else {
            showSystemMessage('Error', result.message || 'Error al guardar el link', 'danger');
        }
    });
}

// Editar link
function editLink(linkId) {
    ajaxRequest('GET', `/agent-journalist/links/read?link_id=${linkId}`, null, function(status, response) {
        if (status === 200) {
            const link = JSON.parse(response).result;
            if (link) {
                document.getElementById('edit_link_id').value = link.id;
                document.getElementById('edit_medio').value = link.medio;
                document.getElementById('edit_titulo').value = link.titulo;
                document.getElementById('edit_link').value = link.link;
                
                const modal = new bootstrap.Modal(document.getElementById('editLinkModal'));
                modal.show();
            }
        } else {
            showSystemMessage('Error', 'No se pudo cargar la información del link', 'danger');
        }
    });
}

// Actualizar link
function updateLink() {
    const linkId = document.getElementById('edit_link_id').value;
    const medio = document.getElementById('edit_medio').value.trim();
    const titulo = document.getElementById('edit_titulo').value.trim();
    const link = document.getElementById('edit_link').value.trim();
    
    if (!medio || !titulo || !link) {
        showSystemMessage('Error', 'Todos los campos marcados con * son obligatorios', 'danger');
        return;
    }
    
    const data = {
        link_id: linkId,
        update_data: {
            medio: medio,
            titulo: titulo,
            link: link
        }
    };
    
    ajaxRequest('PUT', '/agent-journalist/links/update', data, function(status, response) {
        const result = JSON.parse(response);
        if (status === 200 && result.status) {
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editLinkModal'));
            modal.hide();
            
            // Mostrar mensaje y recargar links
            showSystemMessage('Éxito', 'Link actualizado correctamente', 'success');
            loadLinks();
        } else {
            showSystemMessage('Error', result.message || 'Error al actualizar el link', 'danger');
        }
    });
}

// Eliminar link
function deleteLink(linkId) {
    if (confirm('¿Estás seguro de que deseas eliminar este link? Esta acción no se puede deshacer.')) {
        ajaxRequest('DELETE', '/links/delete', { link_id: linkId }, function(status, response) {
            const result = JSON.parse(response);
            if (status === 200 && result.status) {
                showSystemMessage('Éxito', 'Link eliminado correctamente', 'success');
                loadLinks();
            } else {
                showSystemMessage('Error', result.message || 'Error al eliminar el link', 'danger');
            }
        });
    }
}

// Crear nota para un link
function createNoteForLink(linkId) {
    // Redirigir a la página de notas con el ID del link
    window.location.href = `/agent-journalist/notes?link_id=${linkId}`;
}

// Aplicar filtros
function applyFilters() {
    const filterMedio = document.getElementById('filterMedio').value.toLowerCase();
    const filterTitulo = document.getElementById('filterTitulo').value.toLowerCase();
    const filterNota = document.getElementById('filterNota').value;
    
    filteredLinks = allLinks.filter(link => {
        const matchMedio = !filterMedio || link.medio.toLowerCase().includes(filterMedio);
        const matchTitulo = !filterTitulo || link.titulo.toLowerCase().includes(filterTitulo);
        const matchNota = !filterNota || link.nota === filterNota;
        
        return matchMedio && matchTitulo && matchNota;
    });
    
    currentPage = 1;
    renderLinksTable(currentPage);
}

// Limpiar filtros
function clearFilters() {
    document.getElementById('filterMedio').value = '';
    document.getElementById('filterTitulo').value = '';
    document.getElementById('filterNota').value = '';
    
    filteredLinks = [...allLinks];
    currentPage = 1;
    renderLinksTable(currentPage);
}

// Añadir función para ver la nota asociada a un link
function viewNoteForLink(linkId) {
    // Buscar la nota asociada al link
    ajaxRequest('GET', '/agent-journalist/notes/all', null, function(status, response) {
        if(status === 200) {
            const notes = JSON.parse(response).result;
            const noteForLink = notes.find(note => note.id_link === linkId);
            
            if (noteForLink) {
                // Redirigir a la página de notas y abrir el modal de visualización
                window.location.href = `/agent-journalist/notes?view_note=${noteForLink.id}`;
            } else {
                showSystemMessage('Información', 'No se encontró una nota asociada a este link', 'info');
            }
        } else {
            showSystemMessage('Error', 'Error al buscar la nota asociada', 'danger');
        }
    });
}
