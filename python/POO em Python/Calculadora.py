from tkinter import *

def iCalculadora(source, side):
    guardarObj = Frame(source, borderwidth=4, bd=4, bg="powder blue")
    guardarObj.pack(side=side, expand =YES, fill =BOTH)
    return guardarObj

def butao(source, side, text, command=None):
    guardarObj = Button(source, text=text, command=command)
    guardarObj.pack(side=side, expand = YES, fill=BOTH)
    return guardarObj

class app(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.option_add('*Font', 'arial 20 bold')
        self.pack(expand = YES, fill =BOTH)
        self.master.title('Calculadora')

        display = StringVar()
        Entry(self, relief=RIDGE, textvariable=display,
          justify='right'
          , bd=30, bg="powder blue").pack(side=TOP,
                                          expand=YES, fill=BOTH)

        for limparBotao in (["C"]):
            erase = iCalculadora(self, TOP)
            for ichar in limparBotao:
                butao(erase, LEFT, ichar, lambda
                    guardarObj=display, q=ichar: guardarObj.set(''))

        for botaoNum in ("789/", "456*", "123-", "0.+"):
         FunctionNum = iCalculadora(self, TOP)
         for iIgual in botaoNum:
            butao(FunctionNum, LEFT, iIgual, lambda
                guardarObj=display, q=iIgual: guardarObj
                   .set(guardarObj.get() + q))

        IgualBotao = iCalculadora(self, TOP)
        for iIgual in "=":
            if iIgual == '=':
                btniIgual = butao(IgualBotao, LEFT, iIgual)
                btniIgual.bind('<ButtonRelease-1>', lambda e,s=self,
                                guardarObj=display: s.calcular(guardarObj), '+')


            else:
                btniIgual = butao(IgualBotao, LEFT, iIgual,
                                    lambda guardarObj=display, s=' %s ' % iIgual: guardarObj.set
                                    (guardarObj.get() + s))

    def calcular(self, display):
            try:
                display.set(eval(display.get()))
            except:
                display.set("ERROR")

#Iniciar o GUI
if __name__=='__main__':
 app().mainloop()
