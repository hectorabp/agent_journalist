// Función AJAX reutilizable
function ajaxRequest(method, url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            callback(xhr.status, xhr.responseText);
        }
    };
    xhr.send(data ? JSON.stringify(data) : null);
}

// Función para mostrar mensajes del sistema
function showSystemMessage(title, message, type = 'info') {
    const modalTitle = document.getElementById('systemModalTitle');
    const modalBody = document.getElementById('systemModalBody');
    const modal = new bootstrap.Modal(document.getElementById('systemModal'));
    
    modalTitle.textContent = title;
    modalBody.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    modal.show();
}

// Función para formatear fechas
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Función para truncar texto largo
function truncateText(text, maxLength = 50) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Función para crear paginación
function createPagination(totalItems, itemsPerPage, currentPage, containerId, onPageChange) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let html = '<nav><ul class="pagination">';
    
    // Botón anterior
    html += `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}"><a class="page-link" href="#" data-page="${currentPage - 1}">Anterior</a></li>`;
    
    // Páginas
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, startPage + 4);
    
    for (let i = startPage; i <= endPage; i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
    }
    
    // Botón siguiente
    html += `<li class="page-item ${currentPage === totalPages ? 'disabled' : ''}"><a class="page-link" href="#" data-page="${currentPage + 1}">Siguiente</a></li>`;
    
    html += '</ul></nav>';
    container.innerHTML = html;
    
    // Agregar eventos a los enlaces de paginación
    const links = container.querySelectorAll('.page-link');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = parseInt(this.getAttribute('data-page'));
            if (page >= 1 && page <= totalPages && page !== currentPage) {
                onPageChange(page);
            }
        });
    });
}

// Cambio de tema claro/oscuro
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('btnThemeToggle');
    if (themeToggle) {
        // Verificar si hay una preferencia guardada
        const darkMode = localStorage.getItem('darkMode') === 'true';
        if (darkMode) {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="bi bi-sun"></i>';
        }
        
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            themeToggle.innerHTML = isDarkMode ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon"></i>';
        });
    }
});
