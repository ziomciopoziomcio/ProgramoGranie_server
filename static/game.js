const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');
const heartsContainer = document.getElementById('hearts-container');

// Game variables
let bird = { x: 50, y: 150, width: 30, height: 20, gravity: 0.5, lift: -12, velocity: 0, maxFallSpeed: 9 };
let pipes = [];
let frame = 0;
let score = 0;
const pipeGap = 150;
let gameRunning = false;
let lives = 3;

// PNGs for bird and pipes
const birdImg = new Image();
birdImg.src = '/static/assets/game_assets/fb_skin_default.png';
const pipeImg = new Image();
pipeImg.src = '/static/assets/game_assets/fb_pipe_green.png';
const bgImg = new Image();
bgImg.src = '/static/assets/game_assets/fb_bg_regular_1.png';

const gameSoundtrack = new Audio('/static/assets/game_assets/audio/soundtrack_flappy_dante.mp3');
gameSoundtrack.loop = true; // Zapętlenie audio

const jumpSound = new Audio('/static/assets/game_assets/audio/skok.mp3');
const gameOverSound = new Audio('/static/assets/game_assets/audio/przegrana.mp3');

// Update hearts display
function updateHearts() {
    heartsContainer.innerHTML = '';
    for (let i = 0; i < 3; i++) {
        const heart = document.createElement('img');
        heart.className = i < lives ? 'heart_full' : 'heart_empty';
        heartsContainer.appendChild(heart);
    }
}

// Decrease lives
// Decrease lives on the server
async function loseLife() {
    console.log(challengeId);
    try {
        const response = await fetch(`/game/flappy_bird?challenge_id=${challengeId}&action=lose_life`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });

        if (response.ok) {
            const data = await response.json();
            if (data.lives_remaining !== undefined) {
                lives = data.lives_remaining;
                updateHearts();
            } else {
                console.error('Error updating lives:', data.error);
            }
        } else {
            console.error('Failed to update lives:', response.statusText);
        }
    } catch (error) {
        console.error('Error during loseLife request:', error);
    }
}

// Reset lives
function resetLives() {
    lives = 3;
    updateHearts();
}

// Fetch lives from the server
async function fetchLives() {
    try {
        const response = await fetch(`/game/flappy_bird?challenge_id=1`);
        const data = await response.json();
        if (data.lives_remaining !== undefined) {
            lives = data.lives_remaining;
            updateHearts();
        } else {
            console.error('Error fetching lives:', data.error);
        }
    } catch (error) {
        console.error('Error fetching lives:', error);
    }
}

// Send score to backend
function sendScoreToBackend(score) {
    fetch('/submit_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score }),
    }).catch(error => console.error('Error sending score:', error));
}

// Game loop
function update() {
    frame++;
    bird.velocity += bird.gravity;
    if (bird.velocity > bird.maxFallSpeed) bird.velocity = bird.maxFallSpeed;
    if (bird.velocity < bird.lift) bird.velocity = bird.lift;
    bird.y += bird.velocity;

    if (frame % 120 === 0) {
        const pipeHeight = Math.random() * (canvas.height / 2);
        pipes.push({ x: canvas.width, y: pipeHeight, scored: false });
    }

    pipes.forEach(pipe => pipe.x -= 2);

    pipes.forEach(pipe => {
        if (
            bird.x < pipe.x + 50 &&
            bird.x + bird.width > pipe.x &&
            (bird.y < pipe.y || bird.y + bird.height > pipe.y + pipeGap)
        ) {
            endGame();
        }

        if (!pipe.scored && bird.x > pipe.x + 50) {
            score++;
            pipe.scored = true;
        }
    });

    pipes = pipes.filter(pipe => pipe.x + 50 > 0);

    if (bird.y + bird.height > canvas.height || bird.y < 0) {
        endGame();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);
    ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

    pipes.forEach(pipe => {
        for (let y = pipe.y - 200; y > -200; y -= 200) {
            ctx.save();
            ctx.translate(pipe.x + 25, y + 100);
            ctx.rotate(Math.PI);
            ctx.drawImage(pipeImg, -25, -100, 50, 200);
            ctx.restore();
        }

        for (let y = pipe.y + pipeGap; y < canvas.height; y += 200) {
            ctx.drawImage(pipeImg, pipe.x, y, 50, 200);
        }
    });

    if (gameRunning) {
        ctx.fillStyle = '#000';
        ctx.font = 'x-large Tiny5, fantasy';
        ctx.fillText(`SCORE: ${score}`, 10, 20);
    }
}

function resetGame() {
    bird.y = 150;
    bird.velocity = 0;
    pipes = [];
    frame = 0;
    score = 0;
    document.getElementById('hearts-container').style.display = 'flex';
    document.getElementById('game-logo').style.display = 'block';
    updateHearts();
}

function endGame() {
    gameRunning = false;
    canvas.style.display = 'block';
    startButton.style.display = 'block';
    sendScoreToBackend(score);
    loseLife();
    resetGame();
    gameSoundtrack.pause();
    gameSoundtrack.currentTime = 0; // Reset soundtrack to start
    gameOverSound.currentTime = 0; // Reset game over sound to start
    gameOverSound.play();
    draw();
}

function gameLoop() {
    if (gameRunning) {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }
}

// Controls
document.addEventListener('keydown', () => {
    if (gameRunning) {
        jumpSound.currentTime = 0;
        jumpSound.play();
        bird.velocity += bird.lift;
    }
});

window.onload = async () => {
    canvas.style.display = 'block';
    startButton.style.display = 'block';
    startButton.disabled = true;
    await fetchLives();
    startButton.disabled = false;
    draw();
    // debug how many lives we have
    console.log(`Current lives: ${lives}`);

    startButton.textContent = 'ZAGRAJ';
    startButton.style.justifySelf = 'center';
    startButton.style.width = '250px';
    startButton.style.height = '100px';
    startButton.style.backgroundImage = "url('/static/assets/game_assets/play_button.png')";
    startButton.style.backgroundSize = 'cover';
    startButton.style.backgroundPosition = 'center';
    startButton.style.backgroundColor = 'transparent';
    startButton.style.color = 'black';
    startButton.style.border = 'none';
    startButton.style.borderRadius = '12px';
    startButton.style.fontFamily = 'Tiny5, fantasy';
    startButton.style.fontSize = 'x-large';
    startButton.style.cursor = 'pointer';
    startButton.style.transition = 'opacity 0.3s';

    startButton.addEventListener('mouseover', () => {
        startButton.style.opacity = '0.8';
    });

    startButton.addEventListener('mouseout', () => {
        startButton.style.opacity = '1';
    });
};

startButton.addEventListener('click', () => {
    if (lives < 1) {
        alert('Nie masz już żyć!');
        return;
    }
    startButton.style.display = 'none';
    canvas.style.display = 'block';
    gameRunning = true;
    document.getElementById('hearts-container').style.display = 'none';
    document.getElementById('game-logo').style.display = 'none';
    gameSoundtrack.play();
    gameLoop();
});

window.addEventListener('load', () => {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    draw();
});

window.addEventListener('resize', () => {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    draw();

});


// Inicjalizacja gry
document.addEventListener('DOMContentLoaded', () => {
    const selectedBackground = localStorage.getItem('selectedBackground');
    const selectedSkin = localStorage.getItem('selectedSkin');


    console.log('Odczytano z localStorage:', { selectedBackground, selectedSkin });

    // Zastosuj tło
    if (selectedBackground) {
        bgImg.src = selectedBackground; // Ustaw tło gry
        console.log('Ustawiono tło:', selectedBackground);
        // Jeśli tło to bg_hell, ustaw czerwone rury
        if (selectedBackground.includes('bg_hell')) {
            pipeImg.src = '/static/assets/game_assets/fb_pipe_red.png';
            console.log('Ustawiono czerwone rury dla tła bg_hell');
        }
    }

    // Zastosuj skórkę
    if (selectedSkin) {
        birdImg.src = selectedSkin; // Ustaw skórkę gracza
        console.log('Ustawiono skórkę:', selectedSkin);
    }

});