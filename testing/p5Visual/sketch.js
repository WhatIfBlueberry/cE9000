let max = 12;
let scaleFactor = 1;
let matrixSize = 7;
let matrix = [];
distance = 3;

let layer = 0; // global variable
let btnPrev, btnNext;

function setup() {
    createCanvas(windowWidth, windowHeight, WEBGL);
    btnPrev = createButton('←');
    btnNext = createButton('→');
    btnPrev.size(50, 30); // width, height
    btnNext.size(50, 30); // width, height
    btnPrev.position(width / 2 - 30, 30);
    btnNext.position(width / 2 + 30, 30);

    // handle button click events
    btnPrev.mousePressed(() => {
        if (layer < matrixSize - 1) {
            layer++;
        }
    });
    btnNext.mousePressed(() => {
        if (layer > 0) {
            layer--;
        }
    });

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
                    column.push("center");
                } else if (x * x + y * y + z * z <= distance * distance) {
                    column.push("inside");
                } else {
                    column.push("none")
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
                push();
                translate(i, j, z);
                if (z == layer) {
                    if (matrix[i][j][z] == "inside") {
                        fill(0, 0, 255, (alpha = 200));
                        box(0.75);
                        count++;
                    }
                    if (matrix[i][j][z] == "center") {
                        fill(0, 0, 0);
                        box(0.75);
                    }
                    if (matrix[i][j][z] == "none") {
                        fill(255, 0, 0, (alpha = 200));
                        box(0.75);
                    }
                } else {
                    if (matrix[i][j][z] == "inside") {
                        fill(0, 0, 255, (alpha = 10));
                        box(0.75);
                        count++;
                    }
                    if (matrix[i][j][z] == "center") {
                        fill(0, 0, 0);
                        box(0.75);
                    }
                    if (matrix[i][j][z] == "none") {
                        fill(255, 0, 0, (alpha = 10));
                        box(0.75);
                    }
                }
                pop();
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
