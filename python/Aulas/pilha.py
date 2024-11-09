#Estrutura de dados pilha

import numpy as np

#estrutura pilha
class Pilha:

    #construtor da classe pilha
    #os "__" torna a metodo privado na classe
    #O(1)
    def __init__(self,capacidade):
        self.__capacidade = capacidade
        self.__topo = -1 #controlar o topo da pilha
        #cria um vetor vazio do tipo inteiro
        self.__valores = np.empty(self.__capacidade, dtype=int)
        print(self.__capacidade,self.__topo,self.__valores  )

    #os "__" torna a metodo privado na classe
    #avaliar se a pilha está cheia
    #O(1)
    def __pilha_cheia(self): 
        print(self.__capacidade,self.__topo,self.__valores  )
        if self.__topo == self.__capacidade - 1:
            return True
        else:
            return False
    
    #avaliar se a pilha está vazia
    #O(1)
    def __pilha_vazia(self):
        print(self.__capacidade,self.__topo,self.__valores  )
        if self.__topo == -1:
            return True
        else:
            return False
    
    #inserir o elemento na pilha  
    #O(1)  
    def empilhar(self,valor):
        print(self.__capacidade,self.__topo,self.__valores, valor  )
        if self.__pilha_cheia():
            print('A pilha está cheia')
        else:
            self.__topo += 1
            self.__valores[self.__topo] = valor

    #retira o elemento da pilha
    #O(1) apenas 1 operação
    def desempilhar(self):
        print(self.__capacidade,self.__topo,self.__valores  )
        if self.__pilha_vazia():
            print('A pilha está vazia')
        else:
            auxiliar = self.__valores[self.__topo]
            self.__topo -= 1
            return auxiliar

    #não retira o elemento da pilha
    #O(1)
    def ver_topo(self):
        print(self.__capacidade,self.__topo,self.__valores  )
        if self.__topo != -1:
            return self.__valores[self.__topo]
        else:
            return -1

    
 

pilha = Pilha(5) 
print(pilha.ver_topo())
#print(pilha.__pilha_cheia) #erro pois o método é privado da classe
pilha.empilhar(9)
pilha.empilhar(8)
pilha.empilhar(7)
pilha.empilhar(6)
pilha.empilhar(5)
pilha.empilhar(4)
print(pilha.ver_topo())
print(pilha.desempilhar())
pilha.empilhar(77)
print(pilha.ver_topo())
pilha.empilhar(99)