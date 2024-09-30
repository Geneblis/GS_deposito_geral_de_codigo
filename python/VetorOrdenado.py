import numpy as np

class VetorOrdenado:
    def __init__(self, capacidade) -> None:
        self.capacidade = capacidade
        self.ultima_posicao = -1  # Inicializado com -1 para indicar que o vetor está vazio
        self.valores = np.empty(self.capacidade, dtype=int)

    def imprimir(self):
        print(self.capacidade, self.ultima_posicao, self.valores)
        if self.ultima_posicao == -1:
            print("O vetor está vazio")
        else:
            for i in range(self.ultima_posicao + 1):
                print(i, "-", self.valores[i])  # Imprime cada elemento em ordem
    
    def inserir(self, valor):
        if self.ultima_posicao == self.capacidade - 1:
            print("Capacidade maxima antiginda")
            return
        posicao = 0
        for i in range(self.ultima_posicao + 1):
            posicao = 1
            if self.valores[i] > valor:
                break
            if i == self.ultima_posicao:
                posicao = i + 1
        x = self.ultima_posicao
        while x >= posicao:
            self.valores[x+1] = self.valores[x]
            x -= 1

        self.valores[posicao] = valor
        self.ultima_posicao += 1

    def pesquisa_linear(self,valor):
        for i in range(self.ultima_posicao +1):
            if self.valores[i] > valor:
                return -1
            if self.valores[i]==valor:
                return i
            if i == self.ultima_posicao:
                return -1

    def pesquisa_binaria(self, valor):
        limite_inferior = 0
        limite_superior = self.ultima_posicao

        while True:
            posicao_atual = int((limite_inferior + limite_superior)/2)
            if self.valores[posicao_atual] == valor:
                return posicao_atual
            elif limite_inferior > limite_superior:
                return -1
            else:
                if self.valores[posicao_atual] < valor:
                    limite_inferior = posicao_atual + 1
                else:
                    limite_superior = posicao_atual -1

    def excluir(self,valor):
        posicao = self.pesquisar(valor)
        if posicao == -1:
            return -1
        else:
            for i in range(posicao, self.ultima_posicao):
                self.valores[i] = self.valores[i+1]
        self.ultima_posicao -= 1

meuvetor = VetorOrdenado(5)
meuvetor.inserir(10)
meuvetor.inserir(20)
meuvetor.pesquisa_linear(20)
meuvetor.inserir(30)
meuvetor.inserir(40)
meuvetor.inserir(5)
meuvetor.imprimir()
print("--------------")

print(meuvetor.pesquisa_binaria(10))
print(meuvetor.pesquisa_binaria(20))
print(meuvetor.pesquisa_binaria(5))
print(meuvetor.pesquisa_binaria(30))