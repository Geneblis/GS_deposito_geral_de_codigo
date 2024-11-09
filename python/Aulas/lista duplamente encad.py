import numpy as np

class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None
        self.anterior = None
        # |anterior|valor|proximo|

    def mostra_no(self):
        return print(self.valor)
    
class ListaDuplamenteEncadeada:

    def __init__(self):
        self.primeiro = None
        self.ultimo = None
        #|primeiro|ultimo|

    def __lista_vazia(self):
        return self.primeiro == None
    
    def insere_inicio(self,valor):
        novo = No(valor)
        #se a lista estiver vazia self.primeiro e self.ultimo = None
        if self.__lista_vazia():
            self.ultimo = novo
        else:
            self.primeiro.anterior = novo
        novo.proximo = self.primeiro
        self.primeiro = novo

    def insere_final(self, valor):
        novo = No(valor)
        if self.__lista_vazia():
            self.primeiro = novo
        else:
            self.ultimo.proximo = novo
            novo.anterior = self.ultimo
        self.ultimo = novo

    def excluir_inicio(self):
        temp = self.primeiro
        if self.primeiro.proximo == None:
            self.ultimo = None
        else:
            self.primeiro.proximo.anterior = None
        self.primeiro = self.primeiro.proximo
        return temp

    def excluir_final(self):
        temp = self.ultimo
        if self.primeiro.proximo == None:
            self.primeiro = None
        else:
            self.ultimo.anterior.proximo = None
        self.ultimo = self.ultimo.anterior
        return temp

    def excluir_posicao(self,valor):
        atual =self.primeiro
        while atual.valor != valor:
            atual = atual.proximo
            if atual == None:
                #não encontrou o valor
                return
        if atual == self.primeiro: # so existe um elemento
            self.primeiro = atual.proximo
        else:
            atual.anterior.proximo = atual.proximo #primeiro link
        
        if atual == self.ultimo:
            self.ultimo = atual.anterior
        else:
            atual.proximo.anterior = atual.anterior
        
        return atual

    def mostrar_frente(self):
        atual = self.primeiro
        while atual != None:
            atual.mostra_no()
            atual = atual.proximo     

    def mostrar_tras(self):
        atual = self.ultimo
        while atual != None:
            atual.mostra_no()
            atual = atual.anterior








lista = ListaDuplamenteEncadeada()
no1 = No(1)
no2 = No(2)
no3 = No(3)
no4 = No(4)
print(lista.primeiro, lista.ultimo)
print(no1.anterior, no1.valor, no1.proximo)
print(no2.anterior, no2.valor, no2.proximo)
print(no3.anterior, no3.valor, no3.proximo)
print(no4.anterior, no4.valor, no4.proximo)

lista.ultimo = no1
no1.proximo = lista.primeiro
lista.primeiro = no1

no1.anterior = no2
no2.proximo = lista.primeiro
lista.primeiro = no2

no2.anterior = no3
no3.proximo = lista.primeiro
lista.primeiro = no3

no3.anterior = no4
no4.proximo = lista.primeiro
lista.primeiro = no4

print(lista.primeiro.valor, lista.ultimo.valor)

print(lista.mostrar_frente())
print('---')
print(lista.mostrar_tras())

print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')


lde = ListaDuplamenteEncadeada()

lde.insere_inicio(1)
lde.insere_inicio(2)
lde.insere_inicio(3)
lde.insere_inicio(4)
lde.insere_inicio(5)

lde.mostrar_frente()
print('---')


lde.mostrar_tras()
print('---')

print(lde.primeiro.valor, lde.ultimo.valor)

print(lde.primeiro, lde.ultimo)

print('zzzzzzzzzz')

lde = ListaDuplamenteEncadeada()
lde.insere_inicio(1)
lde.insere_inicio(2)
lde.insere_final(3)
lde.insere_final(4)
lde.mostrar_frente()

print('zzzzzzzzzz')

lde.mostrar_tras()
print('pppp')

lde = ListaDuplamenteEncadeada()
lde.insere_inicio(1)
lde.insere_inicio(2)
lde.insere_inicio(3)
lde.insere_inicio(4)
lde.insere_inicio(5)
lde.mostrar_frente()
print('uuuu')


lde.excluir_inicio()
lista.mostrar_frente()
print('ffff')


lista.excluir_final()
lista.mostrar_frente()
print('tttt')

lista.mostrar_tras()

print('uuuuuuuuuuuuuuuuuu')



lde = ListaDuplamenteEncadeada()

lde.insere_inicio(1)
lde.insere_inicio(2)
lde.insere_inicio(3)
lde.insere_inicio(4)
lde.insere_inicio(5)

lde.mostrar_frente()
print('bbbbbbbbbb')


lde.excluir_posicao(3)
lde.mostrar_frente()
print('----------')

lde.excluir_posicao(5)
lde.mostrar_frente()

print('----------')

lde.excluir_posicao(1)
lde.mostrar_frente()