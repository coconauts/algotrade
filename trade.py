import argparse
from lib import DummyExService,  RandomRate, CSVRate, OutOfMoney, OutOfStock, EndOfFeed
from algos.risk_averse import RiskAverse
from algos.pirate import Pirate

ALGORITHMS = {
    'risk_averse': RiskAverse,
    'pirate': Pirate,
}


def trade(algorithm, funds, rate_src=None, iterations=10000, log_rate=100):
    algo = ALGORITHMS.get(algorithm)
    if not algo:
        print("Error: unknown algorithm: {}".format(algorithm))
        exit(0)

    if rate_src:
        rate_generator = CSVRate(rate_src)
    else:
        rate_generator = RandomRate()

    exs = DummyExService(funds, rate_generator)

    print(
        "Starting with: funds={}, stock={}, exrate={}"
        .format(exs.funds(), exs.balance(), exs.exrate())
    )

    algo = algo(exs)

    for iter in range(iterations):
        try:
            exs.step_exrate()
        except EndOfFeed:
            print ("Reached end of CSV feed")
            exit(0)

        try:
            algo.update()
        except OutOfMoney:
            print ("WARNING: out of money")
        except OutOfStock:
            print ("WARNING: out of stock")
        if iter % log_rate == 0:
            print(
                "Iteration {}: funds={}, stock={}, exrate={}"
                .format(iter, exs.funds(), exs.balance(), exs.exrate())
            )
            input("continue?")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithmic trading playground')
    parser.add_argument('algo', type=str,
                        help='algorithm to use')
    parser.add_argument('funds', type=int,
                        help='total funds in your bank account')
    parser.add_argument('--rate_src', type=str,
                        help='csv file to popuate exchange rate')
    parser.add_argument('--log_rate', type=int, default=100,
                        help="Log every x iterations")

    args = parser.parse_args()

    trade(args.algo, args.funds, args.rate_src, log_rate=args.log_rate)
