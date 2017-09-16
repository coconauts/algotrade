import random

INVESTMENT_AMOUNT = 1000


class Static:
    """ Invest and forget """

    def __init__(self, exservice):
        exservice.buy(INVESTMENT_AMOUNT)

    def update(self):
        pass
