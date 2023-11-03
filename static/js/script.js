document.addEventListener("DOMContentLoaded", function () {
    let timer;
    let timeRemaining = 180; 
    
    const container = document.getElementById("puzzle-container");
    const shuffleButton = document.getElementById("shuffle-button");
    const image = new Image();
    let emptyTile = null;
    
    var urlPathname = window.location.pathname;
    var filename = urlPathname.substring(urlPathname.lastIndexOf('/') + 1);
    
    
    function updateTimerDisplay() {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        const timerDisplay = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    
        document.getElementById("timer-display").textContent = timerDisplay;
    
        
        if (timeRemaining <= 0) {
            clearInterval(timer);
            alert("Time's up! You didn't solve the puzzle.");
        }
    }
    
    
    image.src = '../static/images/'+filename; 
    
    
    image.onload = function () {
        const tiles = [];
    
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 3; col++) {
                const tile = document.createElement("div");
                tile.className = "puzzle-tile";
                tile.style.backgroundImage = `url(${image.src})`;
                tile.style.backgroundPosition = `-${col * 100}px -${row * 100}px`;
                tile.style.gridRow = row + 1;
                tile.style.gridColumn = col + 1;
                tiles.push(tile);
            }
        }
    
        
        const lastTile = tiles.pop();
        emptyTile = document.createElement("div");
        emptyTile.className = "empty-tile";
        emptyTile.style.gridRow = "3";
        emptyTile.style.gridColumn = "3";
    
        shuffleTiles(tiles);
    
        tiles.forEach((tile) => {
            tile.addEventListener("click", () => {
                moveTile(tile, tiles);
            });
            container.appendChild(tile);
        });
    
        container.appendChild(emptyTile);
    
        
        updateTimerDisplay(); 
        timer = setInterval(function () {
            timeRemaining--;
            updateTimerDisplay();
        }, 1000); 
    };
    
    
    function stopTimer() {
        clearInterval(timer);
    
    };
    
    function shuffleTiles(tiles) {
        for (let i = tiles.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [tiles[i].style.gridRow, tiles[j].style.gridRow] = [tiles[j].style.gridRow, tiles[i].style.gridRow];
            [tiles[i].style.gridColumn, tiles[j].style.gridColumn] = [tiles[j].style.gridColumn, tiles[i].style.gridColumn];
        }
    
    }
    
    function moveTile(tile, tiles) {
        const tileRow = parseInt(tile.style.gridRow);
        const tileCol = parseInt(tile.style.gridColumn);
        const emptyRow = parseInt(emptyTile.style.gridRow);
        const emptyCol = parseInt(emptyTile.style.gridColumn);
    
        if (
            (Math.abs(tileRow - emptyRow) === 1 && tileCol === emptyCol) ||
            (Math.abs(tileCol - emptyCol) === 1 && tileRow === emptyRow)
        ) {
            [tile.style.gridRow, emptyTile.style.gridRow] = [emptyTile.style.gridRow, tile.style.gridRow];
            [tile.style.gridColumn, emptyTile.style.gridColumn] = [emptyTile.style.gridColumn, tile.style.gridColumn];
        }
    
        if (isPuzzleSolved(tiles)) {
            alert("Congratulations! You solved the puzzle!");
        }
    }
    
    function isPuzzleSolved(tiles) {
        for (let i = 0; i < tiles.length; i++) {
            const tile = tiles[i];
            const correctPosition = {
                row: Math.floor(i / 3) + 1,
                col: (i % 3) + 1,
            };
            if (
                parseInt(tile.style.gridRow) !== correctPosition.row ||
                parseInt(tile.style.gridColumn) !== correctPosition.col
            ) {
                return false;
            }
        }
        return true;
    }
    
    shuffleButton.addEventListener("click", () => {
        
        stopTimer();
        timeRemaining = 180; 
        updateTimerDisplay(); 
        
        updateTimerDisplay(); 
        timer = setInterval(function () {
            timeRemaining--;
            updateTimerDisplay();
        }, 1000); 
    
        const tiles = document.querySelectorAll(".puzzle-tile");
        shuffleTiles(Array.from(tiles));
    });
    
    });