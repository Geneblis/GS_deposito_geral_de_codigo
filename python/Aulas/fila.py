import numpy as np #importar a biblioteca numpy

#criar a classe
class Fila:
    
    #Construtor da classe, que inicializa o vetor vazio.
    #O(1)
    def __init__(self, capacidade): 
        self.capacidade = capacidade 
        self.ultima_posicao = -1    
        #cria um vetor vazio para o tipo inteiro
        self.valores = np.empty(self.capacidade, dtype=int) 
        print(capacidade, self.ultima_posicao, self.valores)  
    
    #metodo enfileirar
    #O(1)
    def enfileirar(self, valor):
        print(self.capacidade, self.ultima_posicao, self.valores, valor) 
        if self.ultima_posicao == self.capacidade - 1:
            print('Capacidade máxima da fila atingida')
        else:
            self.ultima_posicao += 1 
            self.valores[self.ultima_posicao] = valor
            

    #metodo desinfileirar
    #O(n)
    def desinfileirar(self):
        print(self.capacidade, self.ultima_posicao, self.valores)
        if self.ultima_posicao == -1:
            print('Não existe  valores na fila')
        else:
            temp = self.valores[0]
            #deslocando os elementos da fila 
            for i in range(0, self.ultima_posicao):
                self.valores[i] = self.valores[ i + 1]   
        self.ultima_posicao -= 1 #atualiza a ultima posição
        return temp #volta com o valor armazenado

    #metodo ver primeiro
    #O(1)
    def verprimeiro(self):
        print(self.capacidade, self.ultima_posicao,self.valores)
        if self.ultima_posicao == -1:
            print('A fila não possui objetos')      
        else:
            return self.valores[0]
    
    #método imprimir
    #O(n)
    def imprimir(self):
        if self.ultima_posicao == -1:
            print('A fila está vazia')
        else:
            #print(f"Fila ({self.capacidade} elementos):")
            #for i in range(self.ultima_posicao + 1):
            #    print(f"  - Indice: {i}, Valor: {self.valores[i]}")
            #return
            for i in range(self.ultima_posicao + 1):
                print(i, '-', self.valores[i])
            return


fila = Fila(5)
fila.enfileirar(10)
fila.enfileirar(20)
fila.enfileirar(30)
fila.enfileirar(40)
fila.enfileirar(50)
fila.enfileirar(100)
fila.imprimir()
print('---')
print(fila.verprimeiro())
print('desinfileirou: ', fila.desinfileirar())
fila.imprimir()
print('---')
fila.enfileirar(99)
fila.imprimir()
print('---')
print('desinfileirou: ', fila.desinfileirar())
fila.imprimir()
print('---')
print('desinfeleirou: ', fila.desinfileirar())
fila.imprimir()
print('---')
print('desinfileirou: ', fila.desinfileirar())
fila.imprimir()
print('---')
print('desinfileirou: ', fila.desinfileirar())
fila.imprimir()
print('---')
print('desinfileirou: ', fila.desinfileirar())
fila.imprimir()
print('---')

