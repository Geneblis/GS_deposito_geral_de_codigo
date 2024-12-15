const canvas = document.getElementById('board');
const contexto = canvas.getContext('2d');

const LINHAS = 20;
const COLUNAS = 12; // Ajustado para 12 colunas
const TAMANHO_BLOCO = 20;

let tabuleiro = Array.from({ length: LINHAS }, () => Array(COLUNAS).fill(0));
let pontuacao = 0;

const TETROMINOS = [
    [[1, 1, 1, 1]], // I
    [[1, 1], [1, 1]], // O
    [[0, 1, 0], [1, 1, 1]], // T
    [[1, 1, 0], [0, 1, 1]], // S
    [[0, 1, 1], [1, 1, 0]], // Z
    [[1, 0, 0], [1, 1, 1]], // L
    [[0, 0, 1], [1, 1, 1]]  // J
];

let pecaAtual;
let pecaPosicao;

function obterPecaAleatoria() {
    const indiceAleatorio = Math.floor(Math.random() * TETROMINOS.length);
    return TETROMINOS[indiceAleatorio];
}

function desenharTabuleiro() {
    contexto.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < LINHAS; r++) {
        for (let c = 0; c < COLUNAS; c++) {
            if (tabuleiro[r][c]) {
                contexto.fillStyle = 'cyan';
                contexto.fillRect(c * TAMANHO_BLOCO, r * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
                contexto.strokeStyle = 'black';
                contexto.strokeRect(c * TAMANHO_BLOCO, r * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
            }
        }
    }
}

function desenharPeca(peca, posicao) {
    peca.forEach((linha, r) => {
        linha.forEach((valor, c) => {
            if (valor) {
                contexto.fillStyle = 'cyan';
                contexto.fillRect((posicao.x + c) * TAMANHO_BLOCO, (posicao.y + r) * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
                contexto.strokeStyle = 'black';
                contexto.strokeRect((posicao.x + c) * TAMANHO_BLOCO, (posicao.y + r) * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
            }
        });
    });
}

function podeMover(peca, posicao) {
    for (let r = 0; r < peca.length; r++) {
        for (let c = 0; c < peca[r].length; c++) {
            if (peca[r][c]) {
                const novaX = posicao.x + c;
                const novaY = posicao.y + r;
                if (novaX < 0 || novaX >= COLUNAS || novaY >= LINHAS || (novaY >= 0 && tabuleiro[novaY][novaX])) {
                    return false;
                }
            }
        }
    }
    return true;
}

function mesclarPeca(peca, posicao) {
    peca.forEach((linha, r) => {
        linha.forEach((valor, c) => {
            if (valor) {
                tabuleiro[posicao.y + r][posicao.x + c] = 1;
            }
        });
    });
}

function limparLinhas() {
    let linhasLimpa = 0;
    for (let r = LINHAS - 1; r >= 0; r--) {
        if (tabuleiro[r].every(valor => valor === 1)) {
            tabuleiro.splice(r, 1);
            tabuleiro.unshift(Array(COLUNAS).fill(0));
            linhasLimpa++;
        }
    }
    pontuacao += linhasLimpa * 100; // Aumenta a pontuação
    document.getElementById('pontuacao').innerText = `Pontuação: ${pontuacao}`; // Atualiza a pontuação na tela
}

function cairPeca() {
    if (podeMover(pecaAtual, { x: pecaPosicao.x, y: pecaPosicao.y + 1 })) {
        pecaPosicao.y++;
    } else {
        mesclarPeca(pecaAtual, pecaPosicao);
        limparLinhas(); // Limpa linhas completas
        pecaAtual = obterPecaAleatoria();
        pecaPosicao = { x: 3, y: 0 }; // Reinicia a posição da peça

        // Verifica se o jogo acabou
        if (!podeMover(pecaAtual, pecaPosicao)) {
            alert("Fim de jogo! Sua pontuação final foi de: " + pontuacao);
            document.location.reload(); // Reinicia o jogo
        }
    }
    desenharTabuleiro();
    desenharPeca(pecaAtual, pecaPosicao);
}

function moverPeca(direcao) {
    const novaPosicao = { x: pecaPosicao.x + direcao, y: pecaPosicao.y };
    if (podeMover(pecaAtual, novaPosicao)) {
        pecaPosicao = novaPosicao;
    }
    desenharTabuleiro();
    desenharPeca(pecaAtual, pecaPosicao);
}

function girarPeca() {
    const pecaGirada = pecaAtual[0].map((_, index) => pecaAtual.map(linha => linha[index]).reverse());
    if (podeMover(pecaGirada, pecaPosicao)) {
        pecaAtual = pecaGirada;
    }
    desenharTabuleiro();
    desenharPeca(pecaAtual, pecaPosicao);
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        moverPeca(-1);
    } else if (event.key === 'ArrowRight') {
        moverPeca(1);
    } else if (event.key === 'ArrowDown') {
        cairPeca();
    } else if (event.key === ' ') { // Adiciona a rotação ao pressionar a barra de espaço
        girarPeca();
    }
});

// Inicializa o jogo
pecaAtual = obterPecaAleatoria();
pecaPosicao = { x: 3, y: 0 };
setInterval(cairPeca, 1000);

function ola() {
    alert("Boa sorte!");
}
ola();