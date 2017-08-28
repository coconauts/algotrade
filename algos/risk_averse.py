import numpy as np

MIN_TRANSACTION_VALUE = 30
TRANSACTION_FEE_PERCENT = .0025
MIN_INVESTMENT_AMOUNT = 100
MAX_INVESTMENT_AMOUNT = 1000


class RiskAverse:
    def __init__(self, exservice):
        self.exservice = exservice

        initial_balance = exservice.balance()

        if initial_balance == 0:
            self.exservice.buy(MIN_INVESTMENT_AMOUNT * 2)
            initial_balance = MIN_INVESTMENT_AMOUNT * 2

        self.investment_exrate = exservice.exrate()
        self.investment_amount = initial_balance

    def update(self):
        current_balance = self.exservice.balance()
        exrate = self.exservice.exrate()

        current_value = current_balance * exrate
        value_at_investment_time = current_balance * self.investment_exrate
        value_diff = current_value - self.investment_amount

        # If value is up enough to make up for fees, sell
        if value_diff > MIN_TRANSACTION_VALUE:
            # But don't fall over the minimun
            if self.exservice.value() - value_diff > MIN_INVESTMENT_AMOUNT:
                self.exservice.sell(value_diff)

        # If there's been a loss, reinvest
        elif abs(value_diff) < MIN_TRANSACTION_VALUE:
            # But don't invest over the maximun
            if self.exservice.value() + value_diff < MAX_INVESTMENT_AMOUNT:
                self.exservice.buy(abs(value_diff))
