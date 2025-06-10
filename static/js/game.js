// FILE DEDICATED TO SCRIPTS IN GAME_PAGE
// (NOT TO BE MISTAKEN WITH FLAPPY BIRD FILES)

// navigation to challenge page
$(document).ready(function() {
    $('#back-button').on('click', function() {
        window.location.href = '/index/challenge';
    });
});

// Zmienne globalne
let currentBackgroundIndex = 0;

// Funkcja do zmiany tła
function updateBackgroundPreview() {
    const backgroundPreview = document.getElementById('game-background-preview');
    backgroundPreview.src = backgrounds[currentBackgroundIndex];
}

// Obsługa przycisków strzałek
document.getElementById('background-arrow-left').addEventListener('click', () => {
    currentBackgroundIndex = (currentBackgroundIndex - 1 + backgrounds.length) % backgrounds.length;
    updateBackgroundPreview();
});

document.getElementById('background-arrow-right').addEventListener('click', () => {
    currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
    updateBackgroundPreview();
});

// Obsługa przycisku "POTWIERDŹ"
document.querySelector('#game-eq-footer .game-styled-button').addEventListener('click', () => {
    /*alert(`Wybrano tło: ${backgrounds[currentBackgroundIndex]}`);*/
    // Możesz tutaj wysłać dane do backendu, np.:
    // fetch('/save-background', { method: 'POST', body: JSON.stringify({ background: backgrounds[currentBackgroundIndex] }) });
});


// Zmienne globalne
let currentSkinIndex = 0;

// Funkcja do zmiany podglądu skórki
function updateSkinPreview() {
    const skinPreview = document.getElementById('game-skin-preview');
    skinPreview.src = skins[currentSkinIndex];
}

// Obsługa przycisków strzałek dla skórek
document.getElementById('skin-arrow-left').addEventListener('click', () => {
    currentSkinIndex = (currentSkinIndex - 1 + skins.length) % skins.length;
    updateSkinPreview();
});

document.getElementById('skin-arrow-right').addEventListener('click', () => {
    currentSkinIndex = (currentSkinIndex + 1) % skins.length;
    updateSkinPreview();
});

// Obsługa przycisku "POTWIERDŹ" dla skórek
document.querySelector('#game-eq-footer .game-styled-button').addEventListener('click', () => {
    /*alert(`Wybrano skórkę: ${skins[currentSkinIndex]}`);*/
    // Możesz tutaj wysłać dane do backendu, np.:
    // fetch('/save-skin', { method: 'POST', body: JSON.stringify({ skin: skins[currentSkinIndex] }) });
});

// Obsługa przycisku "POTWIERDŹ"
document.querySelector('#game-eq-footer .game-styled-button').addEventListener('click', () => {
    localStorage.setItem('selectedBackground', backgrounds[currentBackgroundIndex]);
    localStorage.setItem('selectedSkin', skins[currentSkinIndex]);

    console.log('Zapisano w localStorage:', {
        background: backgrounds[currentBackgroundIndex],
        skin: skins[currentSkinIndex]
    });

    /*alert(`Wybrano tło: ${backgrounds[currentBackgroundIndex]} i skórkę: ${skins[currentSkinIndex]}`);*/

    location.reload();
});

document.addEventListener('DOMContentLoaded', () => {
    const selectedBackground = localStorage.getItem('selectedBackground');
    const selectedSkin = localStorage.getItem('selectedSkin');

    if (selectedBackground) {
        backgroundPreview.src = selectedBackground; // Ustaw podgląd tła
        bgImg.src = selectedBackground; // Ustaw tło gry
    }

    if (selectedSkin) {
        skinPreview.src = selectedSkin; // Ustaw podgląd skórki
        birdImg.src = selectedSkin; // Ustaw skórkę gracza
    }
});