
// Función para expandir/colapsar cuestionarios
function toggleCard(header) {
    const content = header.nextElementSibling;
    const icon = header.querySelector('.expand-icon');
    
    content.classList.toggle('active');
    icon.classList.toggle('expanded');
}

// Funcionalidad de búsqueda
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.questionnaire-card');
            
            cards.forEach(card => {
                const title = card.querySelector('.questionnaire-title').textContent.toLowerCase();
                if (title.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});