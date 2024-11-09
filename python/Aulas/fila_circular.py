import numpy as np

class FilaCircular:
    
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.inicio = 0 #controlar o inicio da fila
        self.final = -1 #controlar o final da fila
        self.numero_elementos = 0
        self.valores = np.empty(self.capacidade, dtype=int)
        print("cap ",self.capacidade,"ini ",self.inicio,"fim ",self.final,
              "n ele ", self.numero_elementos,self.valores)


    #função privada
    def __fila_vazia(self):
        return self.numero_elementos == 0 #booleano

    #função privada
    def __fila_cheia(self):
        return self.numero_elementos == self.capacidade #booleano
    
    #enfileirar
    #O(1)
    def enfileirar(self,valor):
        print("enfileirar ", "cap ",self.capacidade,"ini ",self.inicio,"fim ",self.final,
              "n ele ",self.numero_elementos,self.valores, valor)
        if self.__fila_cheia():
            print('A fila circular está cheia')
            return
        
        #chegou no final da fila?
        if self.final == self.capacidade - 1:
            self.final = -1
        
        self.final += 1
        self.valores[self.final] = valor
        self.numero_elementos += 1

    #desinfileirar(self):
    #O(1)
    def desinfileirar(self):
        print("desinfileirar ", "cap ",self.capacidade,"ini ",self.inicio,"fim ",self.final,
              "n ele ",self.numero_elementos,self.valores,
              self.valores[self.inicio])
        if self.__fila_vazia():
            print("A fila circular está vazia")
            return

        temp = self.valores[self.inicio] #para voltar com o valor 
        
        self.inicio += 1
        if self.inicio == self.capacidade:
            self.inicio = 0
        self.numero_elementos -= 1
        return temp
    
    def primeiro(self):
        if self.__fila_vazia():
            return -1
        return self.valores[self.inicio]
 
filacir = FilaCircular(5)

filacir.enfileirar(10)
filacir.enfileirar(20)
filacir.enfileirar(30)
filacir.enfileirar(40)
filacir.enfileirar(50)
filacir.enfileirar(60)
filacir.desinfileirar()
print(filacir.primeiro())
filacir.desinfileirar()
print(filacir.primeiro())
filacir.enfileirar(60)
filacir.enfileirar(70)
filacir.enfileirar(80)
filacir.desinfileirar()
filacir.desinfileirar()
filacir.desinfileirar()
filacir.enfileirar(80)
filacir.enfileirar(90)
filacir.enfileirar(100)
filacir.enfileirar(200)