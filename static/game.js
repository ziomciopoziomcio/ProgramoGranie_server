const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');

// Game variables
let bird = { x: 50, y: 150, width: 30, height: 20, gravity: 0.5, lift: -9, velocity: 0, maxFallSpeed: 10 };
let pipes = [];
let frame = 0;
let score = 0;
const pipeGap = 150;
let gameRunning = false;

// PNGs for bird and pipes
const birdImg = new Image();
birdImg.src = '/static/assets/game_assets/fb_skin_default.png';
const pipeImg = new Image();
pipeImg.src = '/static/assets/game_assets/fb_pipe_green.png';
const bgImg = new Image();
bgImg.src = '/static/assets/game_assets/fb_bg_regular_1.png';

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

    // Draw background
    ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);

    // Draw bird
    ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

    // Draw pipes
    pipes.forEach(pipe => {
        // Top pipe (rotated)
        for (let y = pipe.y - 200; y > -200; y -= 200) {
            ctx.save();
            ctx.translate(pipe.x + 25, y + 100); // Move to pipe center
            ctx.rotate(Math.PI); // Rotate 180 degrees
            ctx.drawImage(pipeImg, -25, -100, 50, 200); // Draw rotated pipe
            ctx.restore();
        }

        // Bottom pipe
        for (let y = pipe.y + pipeGap; y < canvas.height; y += 200) {
            ctx.drawImage(pipeImg, pipe.x, y, 50, 200);
        }
        //  // Top pipe with rotation
        // ctx.save();
        // ctx.translate(pipe.x + 25, pipe.y - 100); // Move to pipe center
        // ctx.rotate(Math.PI); // rotate 180 degrees
        // ctx.drawImage(pipeImg, -25, -100, 50, 200); // draw rotated top pipe
        // ctx.restore();
        // ctx.drawImage(pipeImg, pipe.x, pipe.y + pipeGap, 50, 200); // Bottom pipe
    });

    // Draw score only if the game is running
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
}

function endGame() {
    gameRunning = false;
    canvas.style.display = 'block';
    startButton.style.display = 'block';
    sendScoreToBackend(score);
    resetGame();
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
        bird.velocity = bird.lift;
    }
});

window.onload = () => {
    canvas.style.display = 'block';
    startButton.style.display = 'block';
    draw();

    // Change start button styles
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

    // Add hover effect
    startButton.addEventListener('mouseover', () => {
        startButton.style.opacity = '0.8';
    });
    startButton.addEventListener('mouseout', () => {
        startButton.style.opacity = '1';
    });
};

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

window.addEventListener('load', () => {
    const container = canvas.parentElement;

    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;

    canvas.style.display = 'block';
    draw();
});

window.addEventListener('resize', () => {
    const container = canvas.parentElement;

    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    draw();

});
