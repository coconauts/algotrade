""" Based on https://github.com/pirate/bitcoin-trader/
"""

from lib import OutOfMoney, OutOfStock


INITIAL_INVESTMENTS = 10
PROFIT_MARGIN_PERCENT = 0.1
FEE_PERCENTAGE = 0.0149
SAMPLE_LENGTH = 5


class Transaction:
    def __init__(self, kind, price, amount):
        self.kind = kind
        self.price = price
        self.amount = amount


class Pirate:  # Arrr
    def __init__(self, exservice):
        self.exservice = exservice

        self.buys = []
        self.sells = []

        self.transactions = []

    def revert(self, transaction):
        price = transaction.amount * self.exservice.exrate()

        if transaction.kind == 'buy':
            self.exservice.sell(price)
            transaction.kind = 'sell'
        elif transaction.kind == 'sell':
            self.exservice.buy(price)
            transaction.kind = 'buy'

        transaction.price = price

    def update(self):
        # TODO use buy/sell price to account for fees
        current_exrate = self.exservice.exrate()

        # Invest until we have a good sample
        if len(self.transactions) < SAMPLE_LENGTH:
            amount = self.exservice.buy(INITIAL_INVESTMENTS)
            self.transactions.append(
                Transaction(kind='buy', price=INITIAL_INVESTMENTS,
                            amount=amount)
            )
            return

        for transaction in self.transactions:
            current_price = transaction.amount * current_exrate

            try:
                if transaction.kind == 'buy':
                    # Sell if we're going to make enough profit when doing so
                    if current_price > transaction.price + transaction.price * PROFIT_MARGIN_PERCENT:
                        self.revert(transaction)

                    # If it went lower than the buy price, sell so that we dont
                    # loose money
                    elif current_price < transaction.price:
                        self.revert(transaction)

                if transaction.kind == 'sell':
                    # if the value has recovered from the sell price, rebuy
                    if current_price > transaction.price:
                        self.revert(transaction)

                # In every other case... wait for prices to fluctuate!

            except OutOfMoney:
                print ("WARN: out of money")
            except OutOfStock:
                print ("WARN: out of stock")
