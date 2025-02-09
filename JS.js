// Funzione per aprire e chiudere il menu
function toggleMenu() {
    var menu = document.getElementById('side-menu');
    
    // Se il menu è nascosto (right = -250px), lo spostiamo verso destra
    if (menu.style.right === '0px') {
        menu.style.right = '-250px'; // Nascondi il menu
    } else {
        menu.style.right = '0px'; // Mostra il menu
    }
}

// Questa funzione inizializza il menu come nascosto
document.getElementById('side-menu').style.right = '-250px';
