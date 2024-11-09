import numpy as np

class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

    def mostra_no(self):
        print(self.valor)

class Arvbinbusca:
    def __init__(self):
        self.raiz = None
        #apenas para mostrar as ligações
        self.ligacoes = []

    def inserir(self, valor):
        novo = No(valor)
        print(id(novo))
        print()

        #verificar se a árvore está vazia
        if self.raiz == None:
            self.raiz = novo
            #print(self.raiz)
        else:
            atual = self.raiz
            while True:
                pai = atual   
                #verificar para esquerda
                if valor < atual.valor:
                    atual = atual.esquerda
                    if atual == None:
                        pai.esquerda = novo
                        #apenas para mostrar
                        self.ligacoes.append(str(pai.valor) + '->' + str(novo.valor))
                        return 
                else:
                    #verificar para direita
                    atual = atual.direita
                    if atual == None:
                        pai.direita = novo
                        #apenas para mostrar
                        self.ligacoes.append(str(pai.valor) + '->' + str(novo.valor))  
                        return
    
    def pesquisar(self, valor):
        atual = self.raiz
        while atual.valor != valor:
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
            if atual == None:
                return None
        return atual

    #raiz, esquerda, direita
    def pre_ordem(self, no):
        if no != None:
            print(no.valor)
            self.pre_ordem(no.esquerda)
            self.pre_ordem(no.direita)

    #esquerda, raiz, direita
    def em_ordem(self, no):
        if no != None:
            self.em_ordem(no.esquerda)
            print(no.valor)
            self.em_ordem(no.direita)

    #esquerda, direita, raiz
    def pos_ordem(self, no):
        if no != None:
            self.pos_ordem(no.esquerda)
            self.pos_ordem(no.direita)
            print(no.valor)


    #apagar no folha
    def excluir(self,valor):
        if self.raiz == None:
            print('A raiz está vazia')
            return
        
        #encontrar o nó
        atual = self.raiz # é o nó que estou processando
        pai = self.raiz
        e_esquerda = True #controlar se o valor está na esquerda ou direita
        while atual.valor != valor:
            pai = atual
            #esquerda
            if valor < atual.valor:
                e_esquerda = True
                #atual ira armazenar o no a ser excluido
                atual = atual.esquerda
            #direita
            else:
                e_esquerda = False
                atual = atual.direita
            if atual == None:
                return False #não encontrou o valor

        #o nó a ser apagado é uma folha
        if atual.esquerda == None and atual.direita == None:
            if atual == self.raiz:
                self.raiz = None
            elif e_esquerda == True:
                #apenas para mostrar
                self.ligacoes.remove(str(pai.valor) + '->' + str(atual.valor))
                pai.esquerda = None
            else:
               self.ligacoes.remove(str(pai.valor) + '->' + str(atual.valor))
               pai.direita = None     

        # o nó a ser apagado não possui filho na direita
        elif atual.direita == None:

            self.ligacoes.remove(str(pai.valor) + '->' + str(atual.valor))
            self.ligacoes.remove(str(atual.valor) + '->' + str(atual.esquerda.valor))

            if atual == self.raiz:
                self.raiz = atual.esquerda

                self.ligacoes.append(str(self.raiz.valor) + '->' + str(atual.esquerda.valor))  

            elif e_esquerda == True:
                pai.esquerda = atual.esquerda

                self.ligacoes.append(str(pai.valor) + '->' + str(atual.esquerda.valor))  

            else:
                pai.direita = atual.esquerda

                self.ligacoes.append(str(pai.valor) + '->' + str(atual.esquerda.valor))

        #o nó a ser apagado não possui filho na esquerda
        elif atual.esquerda == None:

            self.ligacoes.remove(str(pai.valor) + '->' + str(atual.valor))
            self.ligacoes.remove(str(atual.valor) + '->' + str(atual.direita.valor))

            if atual == self.raiz:
                
                self.ligacoes.append(str(self.raiz.valor) + '->' + str(atual.direita.valor))  
                self.raiz = atual.direita

            elif e_esquerda == True:

                self.ligacoes.append(str(pai.valor) + '->' + str(atual.direita.valor))
                pai.esquerda = atual.direita
            else:
                
                self.ligacoes.append(str(pai.valor) + '->' + str(atual.direita.valor))
                pai.direita = atual.direita

    # O nó possui dois filhos
        else:
            sucessor = self.get_sucessor(atual)

            self.ligacoes.remove(str(pai.valor) + '->' + str(atual.valor))
            self.ligacoes.remove(str(atual.direita.valor) + '->' + str(sucessor.valor))
            self.ligacoes.remove(str(atual.valor) + '->' + str(atual.esquerda.valor))
            self.ligacoes.remove(str(atual.valor) + '->' + str(atual.direita.valor))

            if atual == self.raiz:

                self.ligacoes.append(str(self.raiz.valor) + '->' + str(sucessor.valor))     
            
                self.raiz = sucessor

            elif e_esquerda == True:

                self.ligacoes.append(str(pai.valor) + '->' + str(sucessor.valor))

                pai.esquerda = sucessor

            else:

                self.ligacoes.append(str(pai.valor) + '->' + str(sucessor.valor))

                pai.direita = sucessor
        
            self.ligacoes.append(str(sucessor.valor) + '->' + str(atual.esquerda.valor))
            self.ligacoes.append(str(sucessor.valor) + '->' + str(atual.direita.valor))
        
            sucessor.esquerda = atual.esquerda

        return True

    def get_sucessor(self, no):
        pai_sucessor = no
        sucessor = no
        atual = no.direita
        while atual != None:
            pai_sucessor = sucessor
            sucessor = atual
            atual = atual.esquerda
        if sucessor != no.direita:
            pai_sucessor.esquerda = sucessor.direita
            sucessor.direita = no.direita
        return sucessor
        





arvore = Arvbinbusca()
arvore.inserir(53) #raiz
arvore.inserir(30)
arvore.inserir(14)
arvore.inserir(39)
arvore.inserir(9)
arvore.inserir(23)
arvore.inserir(34)
arvore.inserir(49)
arvore.inserir(72)
arvore.inserir(61)
arvore.inserir(84)
arvore.inserir(79)
print()
print(arvore.ligacoes)
print()
print(arvore.pesquisar(39))
print()
print(arvore.pesquisar(89))
print('PRE ORDEM')

arvore.pre_ordem(arvore.raiz)
print()

print('EM ORDEM')
arvore.em_ordem(arvore.raiz)
print()

print('POS ORDEM')
arvore.pos_ordem(arvore.raiz)
print()
              

print()
print(arvore.ligacoes)
print()
#arvore.excluir(84)
print(arvore.ligacoes)

print()
print(arvore.ligacoes)
print()
#arvore.excluir(9)
print(arvore.ligacoes)

print()
print(arvore.ligacoes)
print()
#arvore.excluir(14)
print(arvore.ligacoes)

print()
#print(arvore.get_sucessor(arvore.raiz).valor)
print

arvore.excluir(72)
print(arvore.ligacoes)
print

arvore.excluir(30)
print(arvore.ligacoes)
print