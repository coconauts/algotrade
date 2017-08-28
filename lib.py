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

    def sell(self, money_value):
        stock_qty = money_value * 1.0 / self.exrate()
        stock_qty = min(stock_qty, self._balance)

        self._balance -= stock_qty
        self._funds += money_value

        if self._balance < 1:
            raise OutOfStockException

        return stock_qty

    def buy(self, money_value):
        money_qty = min(money_value, self._funds)
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


"""
class Coinbase:
    def __init__(self):

        self.client = Client(
            settings.API_KEY,
            settings.API_SECRET,
            api_version=settings.API_VERSION)

    def exrate(self, currency='GBP'):

        exrate = self.client.get_spot_price(currency=currency)['amount']
        print("Exrate {}: {}".format(currency, exrate))
        return float(exrate)

    def payment_methods(self):
        print("Payment methods ", self.client.get_payment_methods())

    def accounts(self):
        # accounts = self.client.get_accounts()
        # for account in accounts.data:
        #    balance = account.balance
        #    print ("%s: %s %s" % (account.name, balance.amount, balance.currency))
        #    print account.get_transactions()
        self.account = self.client.get_primary_account()
        self.balance = float(self.account.balance.amount)
        print ("%s: %s %s" % (self.account.name,
                              self.account.balance.amount, self.account.balance.currency))

    def extract(self, amount):
        if settings.DEBUG:
            print("Method not available on debug mode")
            return

        self.account.sell(amount='0.000001',
                          currency="BTC",
                          payment_method=settings.PAYMENT_ID)

    def invest(self, amount):
        if settings.DEBUG:
            print("Method not available on debug mode")
            return

        self.account.buy(amount='0.000001',
                         currency="BTC",
                         payment_method=settings.PAYMENT_ID)
"""
