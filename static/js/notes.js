// Variables globales
let allNotes = [];
let allCategories = [];
let allLinks = [];
let currentPage = 1;
const itemsPerPage = 10;
let filteredNotes = [];

// Sincronización de carga de datos para evitar inconsistencias en la tabla
let notesLoaded = false;
let categoriesLoaded = false;
let linksLoaded = false;

function tryRenderNotesTable() {
    if (notesLoaded && categoriesLoaded && linksLoaded) {
        filteredNotes = [...allNotes];
        renderNotesTable(currentPage);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const linkId = urlParams.get('link_id');
    const viewNoteId = urlParams.get('view_note');

    notesLoaded = false;
    categoriesLoaded = false;
    linksLoaded = false;

    loadNotes();
    loadCategories();
    loadLinks();
    setupEventListeners();

    // Modal de nueva nota si hay link_id
    if (linkId) {
        setTimeout(() => {
            const addNoteModal = new bootstrap.Modal(document.getElementById('addNoteModal'));
            addNoteModal.show();
            const linkSelect = document.getElementById('link_id');
            if (linkSelect) {
                linkSelect.value = linkId;
            }
        }, 500);
    }

    // Modal de visualización si hay view_note
    if (viewNoteId) {
        setTimeout(() => {
            viewNote(viewNoteId);
        }, 500);
    }
});

// Cargar todas las notas
function loadNotes() {
    ajaxRequest('GET', '/notes/all', null, function(status, response) {
        if(status === 200) {
            allNotes = JSON.parse(response).result;
            notesLoaded = true;
            tryRenderNotesTable();
        } else {
            document.getElementById('notes-table').innerHTML = '<div class="alert alert-danger">Error al cargar notas.</div>';
        }
    });
}

// Cargar categorías
function loadCategories() {
    ajaxRequest('GET', '/categories/all', null, function(status, response) {
        if(status === 200) {
            allCategories = JSON.parse(response).result;
            categoriesLoaded = true;
            populateCategoryDropdowns();
            tryRenderNotesTable();
        }
    });
}

// Cargar links
function loadLinks() {
    ajaxRequest('GET', '/links/all', null, function(status, response) {
        if(status === 200) {
            allLinks = JSON.parse(response).result;
            linksLoaded = true;
            populateLinkDropdown();
            tryRenderNotesTable();
        }
    });
}

// Llenar dropdowns de categorías
function populateCategoryDropdowns() {
    const categorySelects = [document.getElementById('id_categoria'), document.getElementById('filterCategoria')];
    
    categorySelects.forEach(select => {
        if (!select) return;
        
        // Mantener la primera opción y limpiar el resto
        const firstOption = select.options[0];
        select.innerHTML = '';
        if (firstOption) {
            select.appendChild(firstOption);
        }
        
        // Añadir categorías
        allCategories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.categoria;
            select.appendChild(option);
        });
    });
}

// Llenar dropdown de links
function populateLinkDropdown() {
    const linkSelect = document.getElementById('link_id');
    if (!linkSelect) return;
    
    // Mantener la primera opción y limpiar el resto
    const firstOption = linkSelect.options[0];
    linkSelect.innerHTML = '';
    if (firstOption) {
        linkSelect.appendChild(firstOption);
    }
    
    // Filtrar links sin nota
    const linksWithoutNote = allLinks.filter(link => link.nota === 'No');
    
    // Añadir links
    linksWithoutNote.forEach(link => {
        const option = document.createElement('option');
        option.value = link.id;
        option.textContent = `${link.medio} - ${truncateText(link.titulo, 40)}`;
        linkSelect.appendChild(option);
    });
}

// Configurar listeners de eventos
function setupEventListeners() {
    // Botón guardar nueva nota
    const btnSaveNote = document.getElementById('btnSaveNote');
    if (btnSaveNote) {
        btnSaveNote.addEventListener('click', saveNewNote);
    }
    
    // Botón actualizar nota
    const btnUpdateNote = document.getElementById('btnUpdateNote');
    if (btnUpdateNote) {
        btnUpdateNote.addEventListener('click', updateNote);
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

// Renderizar tabla de notas con paginación
function renderNotesTable(page) {
    const tableContainer = document.getElementById('notes-table');
    if (!tableContainer) return;

    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedNotes = filteredNotes.slice(startIndex, endIndex);

    let html = '<table class="table table-hover"><thead><tr>';
    html += '<th>ID</th><th>Título</th><th>Categoría</th><th>Link</th><th>Archivo</th><th>Última Modificación</th><th>Acciones</th>';
    html += '</tr></thead><tbody>';

    if (paginatedNotes.length === 0) {
        html += '<tr><td colspan="7" class="text-center">No se encontraron notas</td></tr>';
    } else {
        paginatedNotes.forEach(function(note) {
            const category = allCategories.find(cat => cat.id === note.id_categoria);
            const categoryName = category ? category.categoria : note.id_categoria;
            const link = allLinks.find(l => l.id === note.id_link);
            const linkInfo = link ? `<a href="${link.link}" target="_blank" title="${link.titulo}">${truncateText(link.medio, 20)}</a>` : 'No asociado';
            html += `<tr>
                <td>${note.id}</td>
                <td>${truncateText(note.titulo, 30)}</td>
                <td>${categoryName}</td>
                <td>${linkInfo}</td>
                <td>${note.nombre_archivo}</td>
                <td>${formatDate(note.ultima_modificacion)}</td>
                <td class="action-buttons">
                    <button class="btn btn-sm btn-outline-primary" onclick="viewNote(${note.id})" title="Ver/Editar">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteNote(${note.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>`;
        });
    }

    html += '</tbody></table>';
    tableContainer.innerHTML = html;

    // Crear paginación
    createPagination(filteredNotes.length, itemsPerPage, page, 'notes-pagination', function(newPage) {
        currentPage = newPage;
        renderNotesTable(currentPage);
    });
}

// Filtros de notas
function applyFilters() {
    const titulo = document.getElementById('filterTitulo').value.trim().toLowerCase();
    const categoria = document.getElementById('filterCategoria').value;
    const fecha = document.getElementById('filterFecha').value;

    filteredNotes = allNotes.filter(note => {
        let match = true;
        // Filtro por título (contiene, insensible a mayúsculas)
        if (titulo) {
            match = match && note.titulo.toLowerCase().includes(titulo);
        }
        // Filtro por categoría (id exacto)
        if (categoria) {
            match = match && String(note.id_categoria) === String(categoria);
        }
        // Filtro por fecha (solo fecha, no hora)
        if (fecha) {
            let noteDate = note.ultima_modificacion;
            let onlyDate = '';
            if (typeof noteDate === 'string') {
                // Si es tipo 'Fri, 01 Aug 2025 09:54:51 GMT' o similar
                if (noteDate.match(/^[A-Za-z]{3},/)) {
                    // Parsear con Date
                    const d = new Date(noteDate);
                    if (!isNaN(d)) {
                        onlyDate = d.toISOString().split('T')[0];
                    } else {
                        onlyDate = noteDate;
                    }
                } else if (noteDate.includes('T')) {
                    onlyDate = noteDate.split('T')[0];
                } else if (noteDate.includes(' ')) {
                    onlyDate = noteDate.split(' ')[0];
                } else {
                    onlyDate = noteDate;
                }
            } else if (noteDate instanceof Date) {
                onlyDate = noteDate.toISOString().split('T')[0];
            }
            // Normalizar ambos a YYYY-MM-DD con ceros a la izquierda
            function pad(n) { return n.toString().padStart(2, '0'); }
            function normalize(dateStr) {
                // Espera 'YYYY-MM-DD'
                const parts = dateStr.split('-');
                if (parts.length === 3) {
                    return `${parts[0]}-${pad(parts[1])}-${pad(parts[2])}`;
                }
                return dateStr;
            }
            const normalizedNoteDate = normalize(onlyDate);
            const normalizedFilterDate = normalize(fecha);
            const isMatch = normalizedNoteDate === normalizedFilterDate;
            match = match && isMatch;
        }
        return match;
    });
    currentPage = 1;
    renderNotesTable(currentPage);
}

function clearFilters() {
    document.getElementById('filterTitulo').value = '';
    document.getElementById('filterCategoria').value = '';
    document.getElementById('filterFecha').value = '';
    filteredNotes = [...allNotes];
    currentPage = 1;
    renderNotesTable(currentPage);
}

// Guardar nueva nota
function saveNewNote() {
    const titulo = document.getElementById('titulo').value.trim();
    let id_categoria = document.getElementById('id_categoria').value;
    const content = document.getElementById('content').value;
    let link_id = document.getElementById('link_id').value;

    if (!titulo || !id_categoria || !link_id) {
        showSystemMessage('Error', 'Todos los campos marcados con * son obligatorios', 'danger');
        return;
    }

    // Convertir a int si es posible
    id_categoria = id_categoria ? parseInt(id_categoria) : null;
    link_id = link_id ? parseInt(link_id) : null;

    const data = {
        titulo: titulo,
        id_categoria: id_categoria,
        content: content,
        link_id: link_id
    };
    if (link_id) data.link_id = link_id;

    ajaxRequest('POST', '/notes/create', data, function(status, response) {
        const result = JSON.parse(response);
        if (status === 200 && result.status) {
            // Cerrar modal y limpiar formulario
            const modal = bootstrap.Modal.getInstance(document.getElementById('addNoteModal'));
            modal.hide();
            document.getElementById('addNoteForm').reset();

            // Mostrar mensaje y recargar notas
            showSystemMessage('Éxito', 'Nota guardada correctamente', 'success');
            loadNotes();
            loadLinks(); // Recargar links por si se actualizó el estado de nota
        } else {
            showSystemMessage('Error', result.message || 'Error al guardar la nota', 'danger');
        }
    });
}

// Ver/Editar nota
function viewNote(noteId) {
    ajaxRequest('GET', `/notes/read?nota_id=${noteId}`, null, function(status, response) {
        if (status === 200) {
            const result = JSON.parse(response).result;
            if (result) {
                // Buscar nombre de categoría
                const category = allCategories.find(cat => cat.id === result.id_categoria);
                const categoryName = category ? category.categoria : result.id_categoria;
                
                // Buscar información del link asociado
                const link = allLinks.find(l => l.id === result.id_link);
                const linkInfo = link ? `<a href="${link.link}" target="_blank">${link.medio} - ${truncateText(link.titulo, 30)}</a>` : 'No asociado';
                
                document.getElementById('viewNoteTitle').textContent = result.titulo;
                document.getElementById('viewNoteCategoria').textContent = categoryName;
                document.getElementById('viewNoteLink').innerHTML = linkInfo;
                document.getElementById('viewNoteFecha').textContent = formatDate(result.ultima_modificacion);
                document.getElementById('edit_nota_id').value = result.id;
                document.getElementById('edit_content').value = result.contenido_txt;
                
                const modal = new bootstrap.Modal(document.getElementById('viewNoteModal'));
                modal.show();
            }
        } else {
            showSystemMessage('Error', 'No se pudo cargar la información de la nota', 'danger');
        }
    });
}

// Actualizar nota
function updateNote() {
    const noteId = document.getElementById('edit_nota_id').value;
    const newContent = document.getElementById('edit_content').value;
    // Si hay campos para editar título, categoría o link, obtén sus valores
    let newTitulo = null;
    let newIdCategoria = null;
    let newIdLink = null;
    const tituloInput = document.getElementById('edit_titulo');
    const categoriaInput = document.getElementById('edit_id_categoria');
    const linkInput = document.getElementById('edit_id_link');
    if (tituloInput) newTitulo = tituloInput.value.trim();
    if (categoriaInput) newIdCategoria = categoriaInput.value ? parseInt(categoriaInput.value) : null;
    if (linkInput) newIdLink = linkInput.value ? parseInt(linkInput.value) : null;

    const data = {
        nota_id: noteId,
        new_content: newContent
    };
    if (newTitulo) data.new_titulo = newTitulo;
    if (newIdCategoria) data.new_id_categoria = newIdCategoria;
    if (newIdLink !== null) data.new_id_link = newIdLink;

    ajaxRequest('PUT', '/notes/edit', data, function(status, response) {
        const result = JSON.parse(response);
        if (status === 200 && result.status) {
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('viewNoteModal'));
            modal.hide();

            // Mostrar mensaje y recargar notas
            showSystemMessage('Éxito', 'Nota actualizada correctamente', 'success');
            loadNotes();
        } else {
            showSystemMessage('Error', result.message || 'Error al actualizar la nota', 'danger');
        }
    });
}

// Eliminar nota
function deleteNote(noteId) {
    if (confirm('¿Estás seguro de que deseas eliminar esta nota? Esta acción no se puede deshacer.')) {
        ajaxRequest('DELETE', '/notes/delete', { nota_id: noteId }, function(status, response) {
            const result = JSON.parse(response);
            if (status === 200 && result.status) {
                showSystemMessage('Éxito', 'Nota eliminada correctamente', 'success');
                loadNotes();
                loadLinks(); // Recargar links por si se actualizó el estado de nota
            } else {
                showSystemMessage('Error', result.message || 'Error al eliminar la nota', 'danger');
            }
        });
    }
}
