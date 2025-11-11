// Canvas setup
const canvas = document.getElementById('tetris');
const ctx = canvas.getContext('2d');
const nextCanvas = document.getElementById('next-piece');
const nextCtx = nextCanvas.getContext('2d');

// Game constants
const ROWS = 20;
const COLS = 12;
const BLOCK_SIZE = 20;
const COLORS = [
    null,
    '#FF0D72', // I
    '#0DC2FF', // J
    '#0DFF72', // L
    '#F538FF', // O
    '#FF8E0D', // S
    '#FFE138', // T
    '#3877FF'  // Z
];

// Tetromino shapes
const SHAPES = [
    [],
    [[1, 1, 1, 1]], // I
    [[2, 0, 0], [2, 2, 2]], // J
    [[0, 0, 3], [3, 3, 3]], // L
    [[4, 4], [4, 4]], // O
    [[0, 5, 5], [5, 5, 0]], // S
    [[0, 6, 0], [6, 6, 6]], // T
    [[7, 7, 0], [0, 7, 7]]  // Z
];

// Game state
let board = [];
let currentPiece = null;
let nextPiece = null;
let score = 0;
let level = 1;
let lines = 0;
let gameRunning = false;
let gamePaused = false;
let dropCounter = 0;
let dropInterval = 1000;
let lastTime = 0;

// Initialize board
function createBoard() {
    return Array.from({ length: ROWS }, () => Array(COLS).fill(0));
}

// Draw a single block
function drawBlock(context, x, y, color) {
    context.fillStyle = color;
    context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
    context.strokeStyle = '#000';
    context.lineWidth = 2;
    context.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

    // Add highlight for 3D effect
    context.fillStyle = 'rgba(255, 255, 255, 0.3)';
    context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE / 4, BLOCK_SIZE);
    context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE / 4);
}

// Draw the board
function drawBoard() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    board.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value > 0) {
                drawBlock(ctx, x, y, COLORS[value]);
            }
        });
    });
}

// Draw the current piece
function drawPiece(piece, context, offsetX = 0, offsetY = 0) {
    piece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value > 0) {
                drawBlock(context, x + piece.x + offsetX, y + piece.y + offsetY, COLORS[value]);
            }
        });
    });
}

// Create a new piece
function createPiece(typeId = null) {
    const id = typeId || Math.floor(Math.random() * 7) + 1;
    return {
        shape: SHAPES[id].map(row => [...row]),
        x: Math.floor(COLS / 2) - Math.floor(SHAPES[id][0].length / 2),
        y: 0,
        id: id
    };
}

// Check collision
function collision(piece, board) {
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x] !== 0) {
                const newX = piece.x + x;
                const newY = piece.y + y;

                if (newX < 0 || newX >= COLS || newY >= ROWS) {
                    return true;
                }

                if (newY >= 0 && board[newY][newX] !== 0) {
                    return true;
                }
            }
        }
    }
    return false;
}

// Merge piece with board
function merge(piece, board) {
    piece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                if (piece.y + y >= 0) {
                    board[piece.y + y][piece.x + x] = value;
                }
            }
        });
    });
}

// Rotate piece
function rotate(piece, direction = 1) {
    const rotated = {
        ...piece,
        shape: piece.shape[0].map((_, i) =>
            piece.shape.map(row => row[i]).reverse()
        )
    };

    // Wall kick
    let offset = 0;
    while (collision(rotated, board)) {
        rotated.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > piece.shape[0].length) {
            return piece; // Can't rotate
        }
    }

    return rotated;
}

// Move piece
function move(piece, dir) {
    piece.x += dir;
    if (collision(piece, board)) {
        piece.x -= dir;
        return false;
    }
    return true;
}

// Drop piece
function drop(piece) {
    piece.y++;
    if (collision(piece, board)) {
        piece.y--;
        return false;
    }
    dropCounter = 0;
    return true;
}

// Hard drop
function hardDrop(piece) {
    let dropDistance = 0;
    while (drop(piece)) {
        dropDistance++;
    }
    return dropDistance;
}

// Clear lines
function clearLines() {
    let linesCleared = 0;

    outer: for (let y = ROWS - 1; y >= 0; y--) {
        for (let x = 0; x < COLS; x++) {
            if (board[y][x] === 0) {
                continue outer;
            }
        }

        // Remove the line
        const row = board.splice(y, 1)[0].fill(0);
        board.unshift(row);
        y++; // Check the same row again
        linesCleared++;
    }

    if (linesCleared > 0) {
        lines += linesCleared;

        // Scoring
        const linePoints = [0, 40, 100, 300, 1200];
        score += linePoints[linesCleared] * level;

        // Level up every 10 lines
        level = Math.floor(lines / 10) + 1;
        dropInterval = Math.max(100, 1000 - (level - 1) * 100);

        updateDisplay();
    }
}

// Update display
function updateDisplay() {
    document.getElementById('score').textContent = score;
    document.getElementById('level').textContent = level;
    document.getElementById('lines').textContent = lines;
}

// Draw next piece
function drawNextPiece() {
    nextCtx.fillStyle = '#000';
    nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);

    if (nextPiece) {
        const tempPiece = { ...nextPiece, x: 0, y: 0 };
        const offsetX = (4 - nextPiece.shape[0].length) / 2;
        const offsetY = (4 - nextPiece.shape.length) / 2;

        tempPiece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value > 0) {
                    drawBlock(nextCtx, x + offsetX, y + offsetY, COLORS[value]);
                }
            });
        });
    }
}

// Game over
function gameOver() {
    gameRunning = false;
    document.getElementById('final-score').textContent = score;
    document.getElementById('game-over').classList.remove('hidden');
    document.getElementById('start-btn').disabled = false;
    document.getElementById('pause-btn').disabled = true;
}

// Start new piece
function newPiece() {
    currentPiece = nextPiece || createPiece();
    nextPiece = createPiece();
    drawNextPiece();

    if (collision(currentPiece, board)) {
        gameOver();
    }
}

// Game loop
function update(time = 0) {
    if (!gameRunning || gamePaused) {
        return;
    }

    const deltaTime = time - lastTime;
    lastTime = time;
    dropCounter += deltaTime;

    if (dropCounter > dropInterval) {
        if (!drop(currentPiece)) {
            merge(currentPiece, board);
            clearLines();
            newPiece();
        }
    }

    draw();
    requestAnimationFrame(update);
}

// Draw everything
function draw() {
    drawBoard();
    if (currentPiece) {
        drawPiece(currentPiece, ctx);
    }
}

// Start game
function startGame() {
    board = createBoard();
    currentPiece = null;
    nextPiece = null;
    score = 0;
    level = 1;
    lines = 0;
    dropCounter = 0;
    dropInterval = 1000;
    lastTime = 0;
    gameRunning = true;
    gamePaused = false;

    document.getElementById('game-over').classList.add('hidden');
    document.getElementById('start-btn').disabled = true;
    document.getElementById('pause-btn').disabled = false;

    updateDisplay();
    newPiece();
    requestAnimationFrame(update);
}

// Pause game
function togglePause() {
    if (!gameRunning) return;

    gamePaused = !gamePaused;
    document.getElementById('pause-btn').textContent = gamePaused ? 'RESUME' : 'PAUSE';

    if (!gamePaused) {
        lastTime = 0;
        requestAnimationFrame(update);
    }
}

// Keyboard controls
document.addEventListener('keydown', event => {
    if (!gameRunning || gamePaused) {
        if (event.key === 'p' || event.key === 'P') {
            togglePause();
        }
        return;
    }

    switch(event.key) {
        case 'ArrowLeft':
            move(currentPiece, -1);
            break;
        case 'ArrowRight':
            move(currentPiece, 1);
            break;
        case 'ArrowDown':
            if (drop(currentPiece)) {
                score += 1;
                updateDisplay();
            }
            break;
        case 'ArrowUp':
            currentPiece = rotate(currentPiece);
            break;
        case ' ':
            event.preventDefault();
            const dropDist = hardDrop(currentPiece);
            score += dropDist * 2;
            updateDisplay();
            merge(currentPiece, board);
            clearLines();
            newPiece();
            break;
        case 'p':
        case 'P':
            togglePause();
            break;
    }

    draw();
});

// Button event listeners
document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('pause-btn').addEventListener('click', togglePause);
document.getElementById('restart-btn').addEventListener('click', startGame);

// Initial draw
drawBoard();
drawNextPiece();
