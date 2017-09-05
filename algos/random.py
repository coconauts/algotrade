import random

TRANSACTION_VALUE = 100


class Random:
    """ Buys and sells stock randomly """

    def __init__(self, exservice):
        self.exservice = exservice

    def update(self):
        coinflip = random.randint(0, 1)

        if coinflip:
            self.exservice.buy(TRANSACTION_VALUE)
        else:
            self.exservice.sell(TRANSACTION_VALUE)
