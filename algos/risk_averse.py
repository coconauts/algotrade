import numpy as np


class RiskAverse:
    def __init__(self, bank, exrate, investment_amount=100):
        self.bank = bank
        self.bank.invest(investment_amount, exrate)
        self.investment_exrate = exrate
        self.investment_amount = investment_amount
        self.acc_gain = 0

    def update(self, exrate):
        current_value = self.bank.stock * exrate
        value_at_investment_time = self.bank.stock * self.investment_exrate
        value_diff = current_value - self.investment_amount
        stock_diff = value_diff * 1.0 / exrate

        # If there's been a gain, extract it. Otherwise noop.
        if value_diff > 0:
            amount = self.bank.extract(stock_diff, exrate)
            self.acc_gain += amount

        # If there's been a loss, reinvest
        elif value_diff < 0:
            self.bank.invest(-1 * value_diff, exrate)
            self.acc_gain += value_diff
