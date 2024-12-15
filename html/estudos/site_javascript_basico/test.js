alert("ola!")
let int = 3;
let cagadas = "Cagadas";
let peso = 0.3;

function somar(a) {
    return a + int
}
let resultado = somar(20);
console.log("Resultado da soma:", resultado);

function subtrair(b) {
    let valor_temp = 10
    return b - valor_temp
}
let resultadoSubtracao = subtrair(15);
console.log("Resultado da subtração:", resultadoSubtracao);

let num1 = 5;
console.log(num1);
console.log(5 != `5`)

function multiplicarArray(arr) {
    let produto = 1;
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr[i].length; j++) {
            produto *= arr[i][j];
        }
    }
    return produto;
}

var produto = multiplicarArray([[1, 5], [4, 6, 7], [33, 6, 9]]);
console.log(produto);