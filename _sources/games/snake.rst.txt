Snake
======

.. raw:: html

  <div id="snake">
  <script src="snakejs.js">  </script>
    <form id="form1" runat="server">
      <p> Use the "Arrows" to change movement directions, "Space" to pause & resume and "Enter" to restart the game. Enjoy! </p>
      <div>
        <canvas id="drawCanvas" width="700" height="450"></canvas>
      </div>
    </form>
    <script>
      $(document).ready(function() {
        //Canvas stuff
        var drawCanvas = $("#drawCanvas")[0];
        var context = drawCanvas.getContext("2d");
        var width = $("#drawCanvas").width();
        var height = $("#drawCanvas").height();

        var cell_width = 15;
        var defaultRun;
        var snake_food;
        var userscore;
        var mySnakeArray;
        var paused

        function start() {
          defaultRun = "right";
          paused = false;
          userscore = 0;

          createSnake();
          createFood();

          if (typeof game_loop != "undefined") clearInterval(game_loop);
          game_loop = setInterval(paintSnake, 70);
          allowPressKeys = true
        }
        start();

        function createSnake() {
          var snakeSize = 3;
          mySnakeArray = [];

          for (var m = 0; m < snakeSize - 1; m++) {
            mySnakeArray.push({
              x: 0,
              y: 20
            });
          }
        }

        function createFood() {
          snake_food = {
            x: Math.round(Math.random() * (width - cell_width) / cell_width),
            y: Math.round(Math.random() * (height - cell_width) / cell_width),
          };
        }

        function paintSnake() {
          context.fillStyle = "#212326";
          context.strokeStyle = "0000ff";
          context.fillRect(0, 0, width, height);
          context.strokeRect(0, 0, width, height);

          var pop_x = mySnakeArray[0].x;
          var pop_y = mySnakeArray[0].y;

          if      (defaultRun == "right") pop_x++;
          else if (defaultRun == "left") pop_x--;
          else if (defaultRun == "down") pop_y++;
          else if (defaultRun == "up")   pop_y--;


          if (pop_x == -1 || pop_x == width / cell_width || pop_y == -1 || pop_y == height / cell_width || check_collision(pop_x, pop_y, mySnakeArray)) {
            start();
            return;
          }

          if (pop_x == snake_food.x && pop_y == snake_food.y) {
            var snake_tail = {
              x: pop_x,
              y: pop_y
            };
            userscore++;
            createFood();
          } else {
            var snake_tail = mySnakeArray.pop();
            snake_tail.x = pop_x;
            snake_tail.y = pop_y;
          }

          mySnakeArray.unshift(snake_tail);

          for (var i = 0; i < mySnakeArray.length; i++) {
            var k = mySnakeArray[i];

            paintCell(k.x, k.y);
          }


          paintCell(snake_food.x, snake_food.y);

          var score_text = "Score: " + userscore;
          context.fillText(score_text, width - 50, 20);
        }

        function paintCell(x, y) {
          context.fillStyle = "#008cba";
          context.strokeStyle = "#212326";
          context.fillRect(x * cell_width, y * cell_width, cell_width, cell_width);
          context.strokeRect(x * cell_width, y * cell_width, cell_width, cell_width);
        }

        function check_collision(x, y, array) {
          for (var i = 0; i < array.length; i++) {
            if (array[i].x == x && array[i].y == y)
              return true;
          }
          return false;
        }

        function togglePause() {
          if      (!paused) {
            paused = true;
            clearInterval(game_loop);
            allowPressKeys = false; }

          else if (paused)  {
            paused = false;
            if (typeof game_loop != "undefined") clearInterval(game_loop);
            game_loop = setInterval(paintSnake, 70);
            allowPressKeys = true}
        }

        function reboot() {
          defaultRun = "right";
          paused = false;
          userscore = 0;

          createSnake();
          createFood();

          if (typeof game_loop != "undefined") clearInterval(game_loop);
          game_loop = setInterval(paintSnake, 70);
          allowPressKeys = true
          }

        $(document).keydown(function(e) {
          var keyInput = e.which;
          if (keyInput == "13") reboot();
          else if (keyInput == "40" && defaultRun != "up") defaultRun = "down";
          else if (keyInput == "39" && defaultRun != "left") defaultRun = "right";
          else if (keyInput == "38" && defaultRun != "down") defaultRun = "up";
          else if (keyInput == "37" && defaultRun != "right") defaultRun = "left";
          else if (keyInput == "32") togglePause();

        })
      })
    </script>
  </div>

**Credits:** This game was created with the help of the following resources: tutorial1_ & tutorial2_



.. _tutorial1 : https://www.c-sharpcorner.com/UploadFile/b5be7f/create-a-classic-snake-game-using-html5-canvas-in-10-simple/
.. _tutorial2 : https://42works.net/technology/snake-game-tutorial-with-html5-canvas-javascript/
