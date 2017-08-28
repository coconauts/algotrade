import numpy as np


class RiskAverse:
    def __init__(self, exservice, investment_amount=100):
        self.exservice = exservice
        if investment_amount is not None:
            self.exservice.buy(investment_amount)
        else:
            investment_amount = exservice.balance()

        self.investment_exrate = exservice.exrate()
        self.investment_amount = investment_amount

    def update(self):
        current_balance = self.exservice.balance()
        exrate = self.exservice.exrate()

        current_value = current_balance * exrate
        value_at_investment_time = current_balance * self.investment_exrate
        value_diff = current_value - self.investment_amount

        # If there's been a gain, extract it. Otherwise noop.
        if value_diff > 0:
            amount = self.exservice.sell(value_diff)

        # If there's been a loss, reinvest
        elif value_diff < 0:
            self.exservice.buy(-1 * value_diff)
