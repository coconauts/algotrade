import argparse
from lib import DummyExService,  RandomRate, CSVRate, OutOfMoney, OutOfStock, EndOfFeed
from algos.simple import Simple
from algos.pirate import Pirate
from algos.random import Random
from algos.static import Static

ALGORITHMS = {
    'simple': Simple,
    'pirate': Pirate,
    'random': Random,
    'static': Static,
}


def trade(algorithm, funds, rate_src=None, iterations=None):
    algo = ALGORITHMS.get(algorithm)
    if not algo:
        print("Error: unknown algorithm: {}".format(algorithm))
        exit(0)

    if rate_src:
        rate_generator = CSVRate(rate_src)
    else:
        rate_generator = RandomRate()

    exs = DummyExService(funds, rate_generator)
    algo = algo(exs)

    step = 0
    initial_exrate = exs.exrate()
    initial_funds = funds

    while True:
        try:
            exs.step_exrate()
        except EndOfFeed:
            break

        try:
            algo.update()
        except OutOfMoney:
            print ("-- WARNING: out of money")
        except OutOfStock:
            print ("-- WARNING: out of stock")

        if iterations and step == iterations:
            break

        step += 1

    # Print report
    final_exrate = exs.exrate()
    final_funds = exs.funds() + exs.balance() * final_exrate
    print(
        "Algorithm: {}\n".format(algorithm),
        "Iterations: {}\n".format(step),
        "Exrate diff: {}\n".format(final_exrate - initial_exrate),
        "Benefit: {}".format(final_funds - initial_funds)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithmic trading playground')
    parser.add_argument('algo', type=str,
                        help='algorithm to use')
    parser.add_argument('funds', type=int,
                        help='total funds in your bank account')
    parser.add_argument('--rate_src', type=str,
                        help='csv file to popuate exchange rate')
    parser.add_argument('--iterations', type=int,
                        help='How many iterations to execute')

    args = parser.parse_args()

    trade(args.algo, args.funds, args.rate_src, args.iterations)
