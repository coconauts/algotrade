import numpy as np
import csv


class OutOfMoneyException(Exception):
    pass


class OutOfStockException(Exception):
    pass


class RateGenerator:
    def __init__(self):
        self._exrate = None
        self.step()

    def exrate(self):
        return self._exrate

    def step(self):
        pass


class RandomRate(RateGenerator):
    def step(self):
        self._exrate = np.random.uniform(low=0.5, high=1.5)


class CSVRate(RateGenerator):
    def __init__(self, csv_file):
        self._rateseq = (row for row in read_csv(csv_file))  # iterator
        self.step()

    def step(self):
        self._exrate = next(self._rateseq)


class DummyExService:
    def __init__(self, funds, rate_generator):
        self._funds = funds
        self._balance = 0
        self.rate_generator = rate_generator

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
        return self.rate_generator.exrate()

    def step_exrate(self):
        self.rate_generator.step()


def read_csv(filename='csv/FB.csv'):
    with open(filename, newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        history = []
        for row in spamreader:
            # Date,Open,High,Low,Close,Adj, Close,Volume
            if row[1] != 'Open':
                history.append(float(row[1]))

        return history
