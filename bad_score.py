import argparse


class MalformedOutput(Exception):
    pass


def score(inp, out):
    raise MalformedOutput("Something went wrong")
    return 0


def solve(seed, inp, log):
    return '0'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp')
    parser.add_argument('ans')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    with open(args.inp, 'r') as f:
        inp = f.read()

    with open(args.ans, 'r') as f:
        ans = f.read()

    print(score(inp, ans))
