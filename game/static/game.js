const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');

// Game variables
let bird = { x: 50, y: 150, width: 20, height: 20, gravity: 0.8, lift: -12, velocity: 0, maxFallSpeed: 10 };
let pipes = [];
let frame = 0;
let score = 0;
const pipeGap = 150;
let gameRunning = false;

// PNGs for bird and pipes
const birdImg = new Image();
birdImg.src = 'https://img.poki-cdn.com/cdn-cgi/image/quality=78,width=1200,height=1200,fit=cover,f=png/5e0df231478aa0a331a4718d09dd91a2.png';
const pipeImg = new Image();
pipeImg.src = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcrdUhqwM_JKKK2yacvaIJ0RpbrPQKLP3CuQ&s';

// Game loop
function update() {
    frame++;
    bird.velocity += bird.gravity;
    if (bird.velocity > bird.maxFallSpeed) bird.velocity = bird.maxFallSpeed; // Limit falling speed
    bird.y += bird.velocity;


    if (frame % 120 === 0) { // PIPE SPAWN RATE!!!
        const pipeHeight = Math.random() * (canvas.height / 2);
        pipes.push({ x: canvas.width, y: pipeHeight, scored: false });
    }

    // Move pipes
    pipes.forEach(pipe => pipe.x -= 2);

    // Collision detection and scoring
    pipes.forEach(pipe => {
        // Check for collision
        if (
            bird.x < pipe.x + 50 &&
            bird.x + bird.width > pipe.x &&
            (bird.y < pipe.y || bird.y + bird.height > pipe.y + pipeGap)
        ) {
            endGame();
        }

        // Check if bird passes the pipe
        if (!pipe.scored && bird.x > pipe.x + 50) {
            score++;
            pipe.scored = true;
        }
    });

    // Remove off-screen pipes
    pipes = pipes.filter(pipe => pipe.x + 50 > 0);

    // Check game borders
    if (bird.y + bird.height > canvas.height || bird.y < 0) {
        endGame();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw bird
    ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

    // Draw pipes
    pipes.forEach(pipe => {
        ctx.drawImage(pipeImg, pipe.x, pipe.y - 200, 50, 200); // Top pipe
        ctx.drawImage(pipeImg, pipe.x, pipe.y + pipeGap, 50, 200); // Bottom pipe
    });

    // Draw score
    ctx.fillStyle = '#000';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 20);
}

function resetGame() {
    bird.y = 150;
    bird.velocity = 0;
    pipes = [];
    frame = 0;
    score = 0;
}

function endGame() {
    gameRunning = false;
    canvas.style.display = 'none';
    startButton.style.display = 'block';
    sendScoreToBackend(score);
    resetGame();
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
        bird.velocity = bird.lift;
    }
});

// Start button event listener
startButton.addEventListener('click', () => {
    startButton.style.display = 'none';
    canvas.style.display = 'block';
    gameRunning = true;
    gameLoop();
});

// Send score to backend (JSON)
function sendScoreToBackend(score) {
    fetch('/submit_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score: score })
    }).then(response => response.json())
      .then(data => console.log('Score submitted:', data))
      .catch(error => console.error('Error submitting score:', error));
}