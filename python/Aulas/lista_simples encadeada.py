#lista encadeada simples

import numpy as np

#criando a classe nó
class No:
    #construtor
    def __init__(self,valor): 
        self.valor = valor
        self.proximo = None #ponteiro
    
    def mostra_no(self):
        print(self.valor)

    def mostra_proximo(self):
        print(self.proximo)

#gerenciador da lista
#armazenar a estrutura de todos os nós
class ListaEncadeada:

    #construtor da classe
    def __init__(self):
        #cabeça da lista = primeiro
        self.primeiro = None #head

    def inserir_inicial(self, valor):
        
        #criamos um novo nó
        novo = No(valor)
        
        #apontamos novo.proximo para primeiro, na primeira vez é None
        novo.proximo = self.primeiro
       
        #apontamos a cabeça para o endereço do novo no
        self.primeiro = novo

    def mostrar(self):
        if self.primeiro == None:
            print('A lista está vazia')
            return None
        
        #criação de um nó auxiliar
        #a lista encadeada começa pelo primeiro
        atual = self.primeiro
        while atual != None:
            atual.mostra_no()
            atual = atual.proximo
            

    def pesquisa(self,valor):
        #pesquisa linear
        if self.primeiro == None:
            print('A lista está vazia')
            return None
        
        #criação de um nó auxiliar
        #cabeça da lista
        atual = self.primeiro #head
        while atual.valor != valor:
            if atual.proximo == None:
                print('A lista está vazia')
                return None
            else:
                atual = atual.proximo
        return atual
    
    def excluir_posicao(self,valor):
        if self.primeiro == None:
            print('A lista está vazia')
            return None
        
        #ambos começam no mesmo nó
        atual = self.primeiro #a avariavel que irá ser eliminada
        anterior = self.primeiro
        #Dois ponteiros são criados e inicializados com o valor do primeiro nó da lista.
        #atual: Esse ponteiro percorre a lista para encontrar o elemento a ser removido.
        #anterior: Esse ponteiro aponta para o nó anterior ao nó que será removido, permitindo a remoção correta do elemento da lista.

        while atual.valor != valor:
            if atual.proximo == None:
                print('O valor não existe na lista')
                return None
            else:
                anterior = atual
                atual = atual.proximo
                
        #fazendo o remanejamento dos ponteiros
        if atual == self.primeiro:
            self.primeiro = self.primeiro.proximo
        else:
            anterior.proximo = atual.proximo
        return atual

    def excluir_inicio(self):
        if self.primeiro == None:
            print('A lista está vazia')
            return None
        temp = self.primeiro #head
        self.primeiro = self.primeiro.proximo
        return temp


print()
lista = ListaEncadeada()
lista.inserir_inicial(10)
print()


lista.inserir_inicial(20)
print()
lista.inserir_inicial(30)
print()
lista.inserir_inicial(40)
print()
lista.inserir_inicial(50)
print()
lista.mostrar()
print()


lista.excluir_inicio()
lista.mostrar()
print('---')

lista.excluir_inicio()
lista.mostrar()
print('---')

lista.excluir_inicio()
lista.mostrar()
print('---')

lista.excluir_inicio()
lista.mostrar()
print('---')

lista.excluir_inicio()
lista.mostrar()
print('---')

lista.mostrar()

lista.inserir_inicial(1)
lista.inserir_inicial(2)
lista.inserir_inicial(3)
lista.inserir_inicial(4)
lista.inserir_inicial(5)
lista.mostrar()
print('---')

pesquisa = lista.pesquisa(3)
if pesquisa != None:
    print('encontrado: ', pesquisa.valor)
else:
    print('não encontrado')

print('---')
lista.excluir_posicao(3)
lista.mostrar()