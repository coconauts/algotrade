import numpy as np


class OutOfMoneyException(Exception):
    pass


class OutOfStockException(Exception):
    pass


class ExratesService:
    """ Exrate here is always from stock to money """
    @staticmethod
    def exrate():
        return np.random.uniform(low=0.5, high=1.5)


class TrustyBank:
    def __init__(self, money):
        self.money = money
        self.stock = 0

    def extract(self, stock_qty, exrate):
        stock_qty = min(stock_qty, self.stock)
        self.stock -= stock_qty
        self.money += stock_qty * exrate
        if self.money < 1:
            raise OutOfMoneyException
        return self.money

    def invest(self, money_qty, exrate):
        money_qty = min(money_qty, self.money)
        self.money -= money_qty
        self.stock += money_qty * 1.0 / exrate
        if self.stock < 1:
            raise OutOfStockException
        return self.stock
