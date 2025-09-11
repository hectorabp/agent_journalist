// Variables globales
let categories = [];
let currentPage = 1;
let itemsPerPage = 10;
let categoryToDelete = null;

// Cargar datos al iniciar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar todas las categorías
    loadCategories();
    
    // Configurar eventos
    document.getElementById('btnSaveCategory').addEventListener('click', saveCategory);
    document.getElementById('btnConfirmDeleteCategory').addEventListener('click', confirmDeleteCategory);
    
    // Resetear el formulario cuando se abre el modal para nueva categoría
    document.getElementById('btnNewCategory').addEventListener('click', function() {
        document.getElementById('categoryForm').reset();
        document.getElementById('categoria_id').value = '';
        document.getElementById('categoryModalTitle').textContent = 'Nueva Categoría';
    });
});

// Función para cargar todas las categorías
function loadCategories() {
    ajaxRequest('GET', '/agent-journalist/categories/all', null, function(status, response) {
        if (status === 200) {
            const data = JSON.parse(response);
            if (data.status) {
                categories = data.result;
                renderCategoriesTable(categories, currentPage);
                createPagination(categories.length, itemsPerPage, currentPage, 'categories-pagination', function(page) {
                    currentPage = page;
                    renderCategoriesTable(categories, currentPage);
                });
            } else {
                showSystemMessage('Error', 'No se pudieron cargar las categorías: ' + data.message, 'danger');
            }
        } else {
            showSystemMessage('Error', 'Error al conectar con el servidor', 'danger');
        }
    });
}

// Función para renderizar la tabla de categorías
function renderCategoriesTable(data, page) {
    const container = document.getElementById('categories-table');
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedData = data.slice(start, end);
    
    if (data.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No hay categorías registradas.</div>';
        return;
    }
    
    let html = `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th class="text-end">Acciones</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    paginatedData.forEach(category => {
        html += `
            <tr>
                <td>${category.id}</td>
                <td>${category.categoria}</td>
                <td class="text-end action-buttons">
                    <button class="btn btn-sm btn-outline-primary" onclick="editCategory(${category.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory(${category.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
}

// Función para guardar una categoría (crear o actualizar)
function saveCategory() {
    const categoriaId = document.getElementById('categoria_id').value;
    const nombre = document.getElementById('categorias').value;
    
    if (!nombre) {
        showSystemMessage('Error', 'El nombre de la categoría es obligatorio', 'warning');
        return;
    }
    
    const data = { categoria: nombre };
    let method, url;
    
    if (categoriaId) {
        // Actualizar categoría existente
        method = 'PUT';
        url = '/agent-journalist/categories/update';
        data.categoria_id = parseInt(categoriaId);
    } else {
        // Crear nueva categoría
        method = 'POST';
        url = '/agent-journalist/categories/create';
    }
    
    ajaxRequest(method, url, data, function(status, response) {
        if (status === 200) {
            const data = JSON.parse(response);
            if (data.status) {
                // Cerrar el modal
                bootstrap.Modal.getInstance(document.getElementById('categoryModal')).hide();
                // Recargar las categorías
                loadCategories();
                // Mostrar mensaje de éxito
                const action = categoriaId ? 'actualizada' : 'creada';
                showSystemMessage('Éxito', `Categoría ${action} correctamente`, 'success');
            } else {
                showSystemMessage('Error', data.message, 'danger');
            }
        } else {
            showSystemMessage('Error', 'Error al conectar con el servidor', 'danger');
        }
    });
}

// Función para editar una categoría
function editCategory(categoriaId) {
    // Buscar la categoría en el array
    const category = categories.find(c => c.id === categoriaId);
    if (!category) return;
    
    // Llenar el formulario con los datos
    document.getElementById('categoria_id').value = category.id;
    document.getElementById('categorias').value = category.categoria;

    // Cambiar el título del modal
    document.getElementById('categoryModalTitle').textContent = 'Editar Categoría';
    
    // Abrir el modal
    new bootstrap.Modal(document.getElementById('categoryModal')).show();
}

// Función para preparar la eliminación de una categoría
function deleteCategory(categoriaId) {
    categoryToDelete = categoriaId;
    new bootstrap.Modal(document.getElementById('deleteCategoryModal')).show();
}

// Función para confirmar la eliminación de una categoría
function confirmDeleteCategory() {
    if (!categoryToDelete) return;
    
    ajaxRequest('DELETE', '/agent-journalist/categories/delete', { categoria_id: categoryToDelete }, function(status, response) {
        if (status === 200) {
            const data = JSON.parse(response);
            if (data.status) {
                // Cerrar el modal
                bootstrap.Modal.getInstance(document.getElementById('deleteCategoryModal')).hide();
                // Recargar las categorías
                loadCategories();
                // Mostrar mensaje de éxito
                showSystemMessage('Éxito', 'Categoría eliminada correctamente', 'success');
            } else {
                showSystemMessage('Error', data.message, 'danger');
            }
        } else {
            showSystemMessage('Error', 'Error al conectar con el servidor', 'danger');
        }
    });
    
    // Resetear la variable
    categoryToDelete = null;
}