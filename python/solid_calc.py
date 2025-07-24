from abc import ABC, abstractmethod
from typing import Dict

# -----------------------------
# SRP: cada classe faz só UMA coisa
# -----------------------------

class InputHandler:
    """Lê e valida a expressão do usuário."""
    def read(self) -> str:
        expr = input("Digite <operador> <n1> <n2> (ex: add 3 5) ou 'sair': ")
        return expr.strip()

class OutputHandler:
    """Exibe resultados ou erros."""
    def show(self, msg: str) -> None:
        print(msg)

# -----------------------------
# OCP & LSP: abstração de operação, extensível sem tocar no parser nem no engine
# -----------------------------

class Operation(ABC):
    """Contrato: toda operação deve receber dois floats e devolver um float."""
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Add(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class Subtract(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class Multiply(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class Divide(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Divisão por zero não permitida")
        return a / b

# -----------------------------
# DIP: a Calculadora depende de abstrações (Operation, InputHandler, OutputHandler)
# -----------------------------

class Calculator:
    """Motor da calculadora: aplica operações cadastradas."""
    def __init__(self,
                 ops: Dict[str, Operation],
                 reader: InputHandler,
                 writer: OutputHandler):
        self.ops    = ops
        self.reader = reader
        self.writer = writer

    def run(self):
        while True:
            cmd = self.reader.read()
            if cmd.lower() == 'sair':
                self.writer.show("Tchau!")
                break

            parts = cmd.split()
            if len(parts) != 3 or parts[0] not in self.ops:
                self.writer.show("Uso: <add|sub|mul|div> <n1> <n2>")
                continue

            op_name, sa, sb = parts
            try:
                a = float(sa); b = float(sb)
                result = self.ops[op_name].execute(a, b)
                self.writer.show(f"Resultado: {result}")
            except ValueError as e:
                self.writer.show(f"Erro: {e}")
            except Exception:
                self.writer.show("Entrada inválida.")

# -----------------------------
# Bootstrap: registra operações e inicia o app
# -----------------------------

def main():
    operations = {
        'add': Add(),
        'sub': Subtract(),
        'mul': Multiply(),
        'div': Divide(),
    }
    calc = Calculator(
        ops    = operations,
        reader = InputHandler(),
        writer = OutputHandler()
    )
    calc.run()

if __name__ == '__main__':
    main()
