
from abc import ABC, abstractmethod
from typing import List

# -----------------------------
# SRP: cada classe faz só UMA coisa
# -----------------------------

class OrderItem:
    """Modelo simples de item de pedido."""
    def __init__(self, name: str, price: float, qty: int = 1):
        self.name = name
        self.price = price
        self.qty = qty

class Order:
    """Gerencia a lista de itens e calcula total bruto."""
    def __init__(self, items: List[OrderItem]):
        self.items = items

    def total(self) -> float:
        return sum(i.price * i.qty for i in self.items)

# -----------------------------
# OCP & LSP: abstração de desconto que pode ser estendida sem mexer no core
# -----------------------------

class DiscountStrategy(ABC):
    """Contrato: qualquer estratégia de desconto deve implementar apply()."""
    @abstractmethod
    def apply(self, order: Order) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, order: Order) -> float:
        return 0.0

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent
    def apply(self, order: Order) -> float:
        # LSP: esse substituto não quebra nada
        return order.total() * (self.percent / 100.0)

class ThresholdDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount: float):
        self.threshold = threshold
        self.discount = discount
    def apply(self, order: Order) -> float:
        return self.discount if order.total() >= self.threshold else 0.0

# -----------------------------
# DIP: processamento depende de abstrações, não de implementações concretas
# -----------------------------

class OrderProcessor:
    """Processa o pedido: calcula total líquido e imprime fatura."""
    def __init__(self, discount_strategy: DiscountStrategy):
        self.discount = discount_strategy

    def process(self, order: Order) -> None:
        bruto = order.total()
        desconto = self.discount.apply(order)
        liquido = bruto - desconto
        self._print_invoice(bruto, desconto, liquido)

    def _print_invoice(self, bruto: float, desconto: float, liquido: float):
        print("----- NOTA FISCAL -----")
        print(f"Total bruto:   R$ {bruto:8.2f}")
        print(f"Desconto:      R$ {desconto:8.2f}")
        print(f"Total líquido: R$ {liquido:8.2f}")
        print("-----------------------\n")

# -----------------------------
# Uso: tudo configurado num único arquivo
# -----------------------------

def main():
    # cria alguns itens
    items = [
        OrderItem("Camiseta", 50.0, 2),
        OrderItem("Calça",    120.0, 1),
        OrderItem("Boné",     35.0, 3),
    ]
    order = Order(items)

    # escolhe a estratégia de desconto (pode trocar sem mudar OrderProcessor)
    # ex1: sem desconto
    p1 = OrderProcessor(NoDiscount())
    p1.process(order)

    # ex2: 10% off
    p2 = OrderProcessor(PercentageDiscount(10))
    p2.process(order)

    # ex3: R$ 50 off a partir de R$ 300
    p3 = OrderProcessor(ThresholdDiscount(threshold=300, discount=50))
    p3.process(order)

if __name__ == "__main__":
    main()
