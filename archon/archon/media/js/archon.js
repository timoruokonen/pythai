var canvasHeight = 600;
var canvasWidth = 600; 
var gridHeight = 100;
var gridWidth = 100;

var image = {
    image: new Image(),
    x: 0,
    y: 0,
    width: 20,
    height: 20,
    oldDir: 0
};

var imageMove = {
    image: new Image(),
    x: 0,
    y: 0,
    width: 20,
    height: 20,
    oldDir: 0
};

var imageBullet0 = new Image();
var imageBullet1 = new Image();
var images = [];
var drawnBullets = [];

var gameOver = false;


function init() {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    image.image.src = 'media/img/red_player.png';
    imageMove.image.src = 'media/img/black_player.png';
    imageBullet0.src = 'media/img/red_bullet.png';
    imageBullet1.src = 'media/img/black_bullet.png';
    images[0] = image;
    images[1] = imageMove;
    setInterval(update, 50);
}


function drawGrid() {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    var gridH = canvasHeight / gridHeight; 
    var gridW = canvasWidth / gridWidth;
    for (var i = 0; i < (gridHeight + 1); i++) {
        ctx.moveTo(0, i * gridH);
        ctx.lineTo(canvasHeight, i * gridH);
        ctx.stroke();
    }
    for (var i = 0; i < (gridWidth + 1); i++) {
        ctx.moveTo(i * gridW,0);
        ctx.lineTo(i * gridW,canvasWidth);
        ctx.stroke();
    }
}

function clear() {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    for (index in images) {
        var x = (images[index].x - 1) * (canvasWidth / gridWidth);
        var y = (images[index].y - 1) * (canvasHeight / gridHeight);
        ctx.clearRect(x, y, images[index].width, images[index].height);
    }
    while (drawnBullets.length > 0) {
        var bullet = drawnBullets.pop();
        var x = (bullet.x - 1) * (canvasWidth / gridWidth);
        var y = (bullet.y - 1) * (canvasHeight / gridHeight);
        ctx.clearRect(x, y, bullet.width, bullet.height);

    }
}

function resetAndStartGame() {
    $.ajax({
        url: 'http://localhost:8000/game/reset',
        success: function(data) {       
            init();    
        },
        error: function(){
            $("#popupcaption").html("Game failed to start.");
            $("#popup").show();
        }
    });
}

function update() {
    if (!gameOver) {
       updatePosition();
    }
    //drawGrid();
}

function updatePosition() {
    $.ajax({
        url: 'http://localhost:8000/game/status',
        success: function(data) {
            clear();
            var game = jQuery.parseJSON(data);
            for (index in game.players) {   
                var player = game.players[index]
                var img = images[player.id];
                //$("#playername" + index).html("Player " + (Number(index) + 1));
                $("#progressbar" + index).progressbar({ value: player.energy});
                if (img == undefined) {
                    console.log(player);
                    //alert("The player does not exist.");
                    break;
                }
                img.x = player.x;
                img.y = player.y;
                draw(img);
            }
            for (index in game.bullets) {
                var bullet = game.bullets[index];
                var bulletImage = {
                        image: undefined,
                        x: bullet.x,
                        y: bullet.y,
                        width: 20,
                        height: 20
                    };
                if (bullet.id == 0) {
                    bulletImage.image = imageBullet0;                        
                }
                else if (bullet.id == 1) {
                    bulletImage.image = imageBullet1;
                }
                draw(bulletImage);
                drawnBullets.push(bulletImage);
            //console.log(bullet.x + ", " + bullet.y);
            }
            if (game.gameOver) {
                gameOver = true;
                console.log("Game over!");
                //alert("Game Over!");
                $("#popupcaption").html("Game over.");
                if (game.winner == 0) {
                    $("#popuptext").html("You lost. The computer won.");
                }
                else {
                    $("#popuptext").html("Congratulations! You won.");    
                }
             $("#popup").show();
            }
      }
    });
} 



function draw(picture) {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    var x = (picture.x) * (canvasWidth / gridWidth);
    var y = (picture.y) * (canvasHeight / gridHeight);
    ctx.drawImage(picture.image, x, y);
}

function move(id, dir) {
    if (images[id].oldDir == dir) {
        return;
    }
    images[id].oldDir = dir;
    $.ajax({
    url: 'http://localhost:8000/game/move/' + id + '/?dir=' + dir,
    success: function(data) {       
        console.log("I am moving " + id + " to " + dir +"!");
    }
    });
}

function shoot(id) {
    var dir = images[id].oldDir;
    $.ajax({
    url: 'http://localhost:8000/game/shoot/' + id + '/?dir=' + dir,
    success: function(data) {       
        console.log("I am shooting " + dir + "!");
    }
    });
}


function clearBullet() {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    var x = (bullet.x - 1) * (canvasWidth / gridWidth);
    var y = (bullet.y - 1) * (canvasHeight / gridHeight);
    ctx.clearRect(x, y, bullet.width, bullet.height);
}


function doKeyDown(evt){
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    switch (evt.keyCode) {
        case 38:  /* Up arrow was pressed */
        move(1, 1);
        break;
        case 40:  /* Down arrow was pressed */
        move(1, 2);
        break;
        case 37:  /* Left arrow was pressed */
        move(1, 4);
        break;
        case 39:  /* Right arrow was pressed */
        move(1, 3);
        break;
        case 32: /* Space bar was pressed */
        shoot(1);
        break;
    }
}

function doKeyUp(evt) {
    if (evt.keyCode != 32) {
        move(1, 0);
    }
}

//The function color not in use. It was used to create the background image for the canvas.
/*
function color() {
    var c=document.getElementById("myCanvas");
    var ctx=c.getContext("2d");
    var grd=ctx.createLinearGradient(0,0,600,600);
    grd.addColorStop(0,"red");
    grd.addColorStop(1,"white");
    ctx.fillStyle=grd;
    ctx.fillRect(0,0,600,600);
}
*/

