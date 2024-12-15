// Constantes
const canvas = document.getElementById('board');
const contexto = canvas.getContext('2d');
const NUM_LINHAS = 20;
const NUM_COLUNAS = 12;
const TAMANHO_BLOCO = 20;
const VELOCIDADE_QUEDA = 1000;
const CORES = { BLOCO: 'cyan', BORDA: 'black' };

// Tetrôminos
const TETROMINOS = [
    [[1, 1, 1, 1]], // I
    [[1, 1], [1, 1]], // O
    [[0, 1, 0], [1, 1, 1]], // T
    [[1, 1, 0], [0, 1, 1]], // S
    [[0, 1, 1], [1, 1, 0]], // Z
    [[1, 0, 0], [1, 1, 1]], // L
    [[0, 0, 1], [1, 1, 1]]  // J
];

// Funções Auxiliares
function desenharBloco(x, y, cor) {
    contexto.fillStyle = cor;
    contexto.fillRect(x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
    contexto.strokeStyle = CORES.BORDA;
    contexto.strokeRect(x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO);
}

function inicializarTabuleiro() {
    return Array.from({ length: NUM_LINHAS }, () => Array(NUM_COLUNAS).fill(0));
}

// Classe Principal
class Tetris {
    constructor() {
        this.tabuleiro = inicializarTabuleiro();
        this.pecaAtual = this.obterPecaAleatoria();
        this.posicaoAtual = { x: 3, y: 0 };
        this.pontuacao = 0;
    }

    obterPecaAleatoria() {
        const indiceAleatorio = Math.floor(Math.random() * TETROMINOS.length);
        return TETROMINOS[indiceAleatorio];
    }

    podeMover(peca, posicao) {
        for (let r = 0; r < peca.length; r++) {
            for (let c = 0; c < peca[r].length; c++) {
                if (peca[r][c]) {
                    const novaX = posicao.x + c;
                    const novaY = posicao.y + r;

                    //nao deixa mover a peca caso para fora da area do jogo.
                    if (novaX < 0 || novaX >= NUM_COLUNAS || novaY >= NUM_LINHAS || (novaY >= 0 && this.tabuleiro[novaY][novaX])) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    mesclarPeca(peca, posicao) {
        peca.forEach((linha, r) => {
            linha.forEach((valor, c) => {
                if (valor) {
                    this.tabuleiro[posicao.y + r][posicao.x + c] = 1;
                }
            });
        });
    }

    limparLinhas() {
        let linhasLimpa = 0;
        for (let r = NUM_LINHAS - 1; r >= 0; r--) {
            if (this.tabuleiro[r].every(valor => valor === 1)) {
                this.tabuleiro.splice(r, 1);
                this.tabuleiro.unshift(Array(NUM_COLUNAS).fill(0));
                linhasLimpa++;
            }
        }
        this.pontuacao += linhasLimpa * 100;
        document.getElementById('pontuacao').innerText = `Pontuação: ${this.pontuacao}`;
    }

    cairPeca() {
        if (this.podeMover(this.pecaAtual, { x: this.posicaoAtual.x, y: this.posicaoAtual.y + 1 })) {
            this.posicaoAtual.y++;
        } else {
            this.mesclarPeca(this.pecaAtual, this.posicaoAtual);
            this.limparLinhas();
            this.pecaAtual = this.obterPecaAleatoria();
            this.posicaoAtual = { x: 3, y: 0 };

            if (!this.podeMover(this.pecaAtual, this.posicaoAtual)) {
                alert("Fim de jogo! Sua pontuacao final foi de: " + this.pontuacao);
                document.location.reload();
            }
        }
        this.atualizarTela();
    }

    moverPeca(direcao) {
        const novaPosicao = { x: this.posicaoAtual.x + direcao, y: this.posicaoAtual.y };
        if (this.podeMover(this.pecaAtual, novaPosicao)) {
            this.posicaoAtual = novaPosicao;
        }
        this.atualizarTela();
    }

    girarPeca() {
        const pecaGirada = this.pecaAtual[0].map((_, index) => this.pecaAtual.map(linha => linha[index]).reverse());
        if (this.podeMover(pecaGirada, this.posicaoAtual)) {
            this.pecaAtual = pecaGirada;
        }
        this.atualizarTela();
    }

    atualizarTela() {
        contexto.clearRect(0, 0, canvas.width, canvas.height);
        this.tabuleiro.forEach((linha, r) => {
            linha.forEach((valor, c) => {
                if (valor) {
                    desenharBloco(c, r, CORES.BLOCO);
                }
            });
        });
        this.desenharPeca(this.pecaAtual, this.posicaoAtual);
    }

    desenharPeca(peca, posicao) {
        peca.forEach((linha, r) => {
            linha.forEach((valor, c) => {
                if (valor) {
                    desenharBloco(posicao.x + c, posicao.y + r, CORES.BLOCO);
                }
            });
        });
    }

    iniciar() {
        setInterval(() => this.cairPeca(), VELOCIDADE_QUEDA);
        this.atualizarTela();
    }
}

// Inicialização
const jogo = new Tetris();
jogo.iniciar();

// Adiciona um listener para as teclas pressionadas
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        jogo.moverPeca(-1);
    } else if (event.key === 'ArrowRight') {
        jogo.moverPeca(1);
    } else if (event.key === 'ArrowDown') {
        jogo.cairPeca();
    } else if (event.key === ' ') {
        jogo.girarPeca();
    }
});

// Função de boas-vindas
function ola() {
    alert("Boa sorte!");
}
ola();