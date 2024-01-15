let missCount = 0;
let score = 0;

function createSpider() {
    const newSpider = document.createElement('div');
    newSpider.classList.add('spider');

    const maxX = window.innerWidth - 150;
    const maxY = window.innerHeight - 150;

    const randomX = Math.random() * maxX;
    const randomY = Math.random() * maxY;

    newSpider.style.transform = `translate(${randomX}px, ${randomY}px)`;

    newSpider.addEventListener('click', (event) => {
        event.stopPropagation(); // Stop the event from propagating to the document click event
        newSpider.remove();
        updateScore();
    });

    spidersContainer.appendChild(newSpider);
}

document.addEventListener('click', () => {
    // Missed the spider
    updateMiss();
});

function updateScore() {
    score += 1;
    const scoreElement = document.getElementById('score');
    scoreElement.textContent = score;

    if (score === 10) {
        showResultDialog('You Won!');
    }
}

function updateMiss() {
    missCount += 1;
    const missElement = document.getElementById('misses');
    missElement.textContent = missCount;

    if (missCount === 5) {
        showResultDialog('You Lost!');
    }
}

function showResultDialog(message) {
    alert(message);
    resetGame();
}

function resetGame() {
    missCount = 0;
    score = 0;
    const scoreElement = document.getElementById('score');
    scoreElement.textContent = '0';

    const missElement = document.getElementById('misses');
    missElement.textContent = '0';

    spidersContainer.innerHTML = '';

    // Start creating spiders again
    createSpider();
}

const spidersContainer = document.querySelector('.spiders-container');

createSpider();



const cursor = document.querySelector('.cursor');

document.addEventListener('mousemove', (e) => {
    cursor.style.left = `${e.clientX - cursor.clientWidth / 2}px`;
    cursor.style.top = `${e.clientY - cursor.clientHeight / 2}px`;
});

document.addEventListener('mousedown', () => {
    cursor.style.backgroundImage = 'url("{{ url_for("static", filename="hammer_45.png") }}")';
});

document.addEventListener('mouseup', () => {
    cursor.style.backgroundImage = 'url("{{ url_for("static", filename="hammer_0.png") }}")';
});

// ... (rest of your existing code)
