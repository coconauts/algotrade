import argparse
from lib import DummyExService
from algos.risk_averse import RiskAverse

ALGORITHMS = {
    'risk_averse': RiskAverse
}


def trade(algorithm, funds, iterations=10000, log_rate=100):
    algo = ALGORITHMS.get(algorithm)
    if not algo:
        print("Error: unknown algorithm: {}".format(algorithm))
        exit(0)

    exs = DummyExService(funds)
    algo = RiskAverse(exs)
    print(
        "Starting with: funds={}, stock={}, exrate={}"
        .format(exs.funds(), exs.balance(), exs.exrate())
    )

    for iter in range(iterations):
        exs.step_exrate()
        algo.update()
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
    parser.add_argument('--log_rate', type=int, default=100,
                        help="Log every x iterations")
    args = parser.parse_args()

    trade(args.algo, args.funds, log_rate=args.log_rate)
