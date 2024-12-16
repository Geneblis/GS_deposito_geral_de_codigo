from tkinter import *

class Calculadora(Frame):
    def __init__(self):
        # Inicializa a classe pai Frame antes da calculadora.
        super().__init__() 
        
        # Configuração da janela principal
        self.master.title("Calculadora")
        self.pack(expand=YES, fill=BOTH)
        #expand=YES: Faz com que o widget "cresça" para ocupar o espaço extra disponível.
        #fill=BOTH: Faz com que o widget ocupe todo o espaço disponível na largura e altura.
        
        # Variável que controla o visor da calculadora
        self.display_var = StringVar()

        """    
        Aqui, self.display_var é um atributo da instância da classe Calculadora.
        Você usa self para garantir que ele seja acessível em qualquer outro método da classe.
        Se você não usasse self, o Python acharia que a variável é apenas local dentro do método e não poderia ser acessada em outros métodos.
        """

        # Visor da calculadora (caixa de texto)
        Entry(self, textvariable=self.display_var, font="Arial 20 bold", justify='right', bd=20, bg="powder blue").pack(
            side=TOP, expand=YES, fill=BOTH
        )

        # Botão de limpar (C)
        self._criar_botao_linha(["C"], self._limpar_display)
        
        # Botões de números e operadores
        botoes = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "+", "="],
        ]
        for linha in botoes:
            self._criar_botao_linha(linha, self._pressionar_botao)

    def _criar_botao_linha(self, botoes, comando):
        """Cria uma linha de botões."""
        linha = Frame(self)
        linha.pack(side=TOP, expand=YES, fill=BOTH)
        for texto in botoes:
            Button(
                linha, text=texto, font="Arial 20 bold", command=lambda t=texto: comando(t)
            ).pack(side=LEFT, expand=YES, fill=BOTH)

            """
            Frame: organiza os botões em linhas horizontais.
            Button: cria um botão para cada texto (número ou operador).
            command: define o que acontece quando o botão é pressionado.
            """

    def _limpar_display(self, _=None):
        self.display_var.set("")

    def _pressionar_botao(self, texto):
        """Adiciona texto ao visor ou calcula o resultado."""
        if texto == "=":
            self._calcular_resultado()
        else:
            self.display_var.set(self.display_var.get() + texto)

    def _calcular_resultado(self):
        """Calcula o resultado da expressão no visor."""
        try:
            resultado = eval(self.display_var.get())  # Avalia a expressão matemática
            self.display_var.set(str(resultado))
        except Exception:
            self.display_var.set("ERROR")  # Em caso de erro

if __name__ == '__main__':
    root = Tk()
    Calculadora().mainloop()
