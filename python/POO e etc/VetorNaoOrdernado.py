import numpy as np #importar a biblioteca numpy

#criar a classe
class VetorNaoOrdenado:
    
    #Construtor da classe, que inicializa o vetor vazio.
    def __init__(self, capacidade): 
        self.capacidade = capacidade #atributo para guardar a capacidade
        self.ultima_posicao = -1 #atribudo (variavel) para guardar a ultima posição
        #cria um vetor vazio do tipo inteiro
        self.valores = np.empty(self.capacidade, dtype = int) 

    #método imprimir para teste
    def imprimir(self): #não recebe nenhum parametro
        if self.ultima_posicao == -1:
            print('O vetor está vazio')
        else:
            for i in range(self.ultima_posicao + 1):
                print(i, '-', self.valores[i])
    
    #metodo inserir
    def inserir(self, valor):
        if self.ultima_posicao == self.capacidade -1:
            print('Capacidade máxima atingida')
        else:
            self.ultima_posicao += 1
            self.valores[self.ultima_posicao] = valor            

    #metodo pesquisar
    def pesquisar(self, valor):
        for i in range(self.ultima_posicao + 1):
            if valor == self.valores[i]:
                return i # o valor existe no vetor
        return -1        # o valor não existe no vetor

    #metodo excluir
    def excluir(self, valor):
        posicao = self.pesquisar(valor)
        if posicao == -1:
            return -1 #não existe o valor no vetor
        else:
            #organizando o vetor -> eliminando o indice vazio
            for i in range(posicao, self.ultima_posicao):
                self.valores[i] = self.valores[ i + 1]
        
        self.ultima_posicao -= 1 #atualiza a ultima posição

meuvetor = VetorNaoOrdenado(3)
meuvetor.inserir(2) 
meuvetor.inserir(3)
meuvetor.pesquisar(3)
meuvetor.inserir(4)
meuvetor.excluir(3)
meuvetor.inserir(5)
meuvetor.inserir(6)
meuvetor.inserir(9)
meuvetor.imprimir()
