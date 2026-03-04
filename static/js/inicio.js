
/*
document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('template_color');

    const colorMap = {
        'blue': 'blue-selected',
        'brown_white': 'brown_white-selected',
        'green': 'green-selected',
        'white_blue': 'white_blue-selected'
    };

    function updateSelectColor() {
        const selectedValue = selectElement.value;
        const newClass = colorMap[selectedValue];
        for (const key in colorMap) {
            selectElement.classList.remove(colorMap[key]);
        }
        if (newClass) {
            selectElement.classList.add(newClass);
        }
    }

    updateSelectColor();
    selectElement.addEventListener('change', updateSelectColor);
});
*/

// Funcionalidad del menú desplegable
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const closeMenu = document.getElementById('closeMenu');
    const menuOverlay = document.getElementById('menuOverlay');
    const menuLinks = document.querySelectorAll('.menu-list a');

    // Abrir menú
    function openMenu() {
        menuToggle.classList.add('active');
        sidebarMenu.classList.add('active');
        menuOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    // Cerrar menú
    function closeMenuFunc() {
        menuToggle.classList.remove('active');
        sidebarMenu.classList.remove('active');
        menuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Event listeners
    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (sidebarMenu.classList.contains('active')) {
                closeMenuFunc();
            } else {
                openMenu();
            }
        });
    }

    if (closeMenu) {
        closeMenu.addEventListener('click', closeMenuFunc);
    }

    if (menuOverlay) {
        menuOverlay.addEventListener('click', closeMenuFunc);
    }

    // Cerrar menú al hacer clic en un enlace
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Si es un enlace interno (con #), cerrar el menú después de un pequeño delay
            if (this.getAttribute('href').startsWith('#')) {
                setTimeout(closeMenuFunc, 300);
            } else {
                closeMenuFunc();
            }
        });
    });

    // Cerrar menú con la tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebarMenu.classList.contains('active')) {
            closeMenuFunc();
        }
    });
});
