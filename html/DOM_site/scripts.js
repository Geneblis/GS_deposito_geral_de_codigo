document.addEventListener("DOMContentLoaded", function() {
    let cabecalho = document.getElementById("meu-txt")
    let quadrado = document.getElementById("quadrado")

    cabecalho.innerText = "Texto Atualizado"
    cabecalho.style.color = "blue"
    cabecalho.style.fontSize = "40px"
    cabecalho.style.fontFamily = "Arial"
    cabecalho.style.backgroundColor = "red"

    function mudarCor(){
        quadrado.style.backgroundColor = "green"
    }

    function desfazerCor(){//bruh
        quadrado.style.backgroundColor = "cyan"
    }

    function diminuirTamanho(){
        quadrado.style.height = "100px"
        quadrado.style.width = "100px"
    }
    function defaultTamanho(){
        quadrado.style.height = "500px"
        quadrado.style.width = "500px"
    }

    window.mudarCor = mudarCor;
    window.desfazerCor = desfazerCor;
    window.diminuirTamanho = diminuirTamanho;
    window.defaultTamanho = defaultTamanho;
});