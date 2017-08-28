import numpy as np


class OutOfMoneyException(Exception):
    pass


class OutOfStockException(Exception):
    pass


class DummyExService:
    def __init__(self, funds):
        self._funds = funds
        self._balance = 0
        self.step_exrate()

    def balance(self):
        return self._balance

    def funds(self):
        return self._funds

    def sell(self, amount):
        stock_qty = amount * 1.0 / self.exrate()
        stock_qty = min(stock_qty, self._balance)

        self._balance -= stock_qty
        self._funds += amount

        if self._balance < 1:
            raise OutOfStockException

        return stock_qty

    def buy(self, amount):
        money_qty = min(amount, self._funds)
        stock_qty = money_qty * 1.0 / self.exrate()

        self._funds -= money_qty
        self._balance += stock_qty

        if self._funds < 1:
            raise OutOfMoneyException

        return stock_qty

    def exrate(self):
        return self._exrate

    def step_exrate(self):
        self._exrate = np.random.uniform(low=0.5, high=1.5)
