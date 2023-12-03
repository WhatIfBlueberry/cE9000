let max = 12;
let scaleFactor = 1;
let matrixSize = 11
let matrix = [];
distance = 3;


function setup() {
    createCanvas(windowWidth, windowHeight, WEBGL);
    scaleFactor = width / max / 2;
    strokeWeight(0);
    fillMatrix();
    frameRate(240);
}


function draw() {
    orbitControl();
    scale(scaleFactor, -scaleFactor, scaleFactor);
    background(160);
    printMatrix();
}

function fillMatrix() {
  matrix = [];
  for (let x = -Math.floor(matrixSize / 2); x < matrixSize; x++) {
      let row = [];
      for (let y = -Math.floor(matrixSize / 2); y < matrixSize; y++) {
          let column = [];
          for (let z = -Math.floor(matrixSize / 2); z < matrixSize; z++) {
            if (x == 0 && y == 0 && z == 0) {
                column.push('center');
            }
            // if distance between x,y,z and 0,0,0 is less than 3
            if (x*x + y*y + z*z <= distance*distance) {
                column.push('in');
            }
            else {
                column.push('none');
              }
          }
          row.push(column);
      }
      matrix.push(row);
  }
}

function printMatrix() {
    count = 0;
    for (let i = 0; i < matrixSize; i++) {
        for (let j = 0; j < matrixSize; j++) {
            for (let z = 0; z < matrixSize; z++) {
              push()
              translate(i, j, z)
              if (matrix[i][j][z] == 'in') {
                    fill(0, 70, 80, alpha=150);
                    box(.4);
                    count++;
              }
              if (matrix[i][j][z] == 'center') {
                    fill(0, 0, 0);
                    box(.4);
              }
              pop()
            }
        }
    }
    print(count);
}

function clearScreen() {
    clear();
    background(0);
}

function drawGrid() {
    stroke(255, 0, 0);
    line(-max, 0, 0, max, 0, 0);
    stroke(0, 255, 0);
    line(0, -max, 0, 0, max, 0);
    stroke(0, 0, 255);
    line(0, 0, -max, 0, 0, max);
}
