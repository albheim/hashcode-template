#!/usr/bin/env pypy2
import argparse
import random
import glob


def parse(inp):
    lines = inp.split('\n')
    R, C, F, N, B, T = map(int, lines[0].split())

    customers = [None for i in range(N)]
    for i in range(N):
        a, b, x, y, s, f = map(int, lines[i + 1].split())
        customers[i] = argparse.Namespace(a=a, b=b, x=x, y=y, s=s, f=f)

    return argparse.Namespace(R=R, C=C, F=F, N=N, B=B, T=T, customers=customers)


def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    print(ns)

    return '0'


def show(out):
    # TODO: Print the solution here
    print(out)


def score(inp, out):
    ns = parse(inp)

    out = "2 2 1\n1 0"

    rides = ns.customers

    lines = out.split('\n')
    cars = [map(int, lines[i].split()[1:]) for i in range(len(lines))]

    cars_time = [0 for _ in range(ns.F)]
    cars_idx = [0 for _ in range(ns.F)]

    score = 0

    for t in range(ns.T):
        # print("time", t)
        for i in range(ns.F):
            # print("car", i)
            if cars_idx[i] < len(cars[i]) and t == cars_time[i]:
                # pick next ride
                x = y = 0
                if cars_idx[i] != 0:
                    ride1 = rides[cars[i][cars_idx[i] - 1]]
                    x, y = ride1.x, ride1.y
                # print(rides[cars[i][cars_idx[i]]])
                ride2 = rides[cars[i][cars_idx[i]]]
                cars_idx[i] += 1

                # calc time to finish next ride
                dist = abs(x - ride2.a) + abs(y - ride2.b)
                dist2 = abs(ride2.x - ride2.a) + abs(ride2.y - ride2.b)
                wait_time = max(0, ride2.s - t - dist)

                cars_time[i] += dist + dist2 + wait_time

                if cars_time[i] <= ns.T:
                    if ride2.s >= t + dist:
                        # print("bonus", ns.B)
                        score += ns.B
                    if cars_time[i] <= ride2.f:
                        # print("normal", dist2)
                        score += dist2


    # print(score)
    return score


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    parser.add_argument('ans', nargs='?')
    parser.add_argument('-s', action='store_true', help="show")
    return parser.parse_args()


def ans2in(ans):
    return ans.replace('.ans', '.in').replace('submission/', 'in/')


def in2ans(inp):
    return inp.replace('.in', '.ans').replace('in/', 'submission/')


if __name__ == '__main__':
    args = get_args()
    if not args or (not args.inp and not args.ans):
        files = []
        for ans in glob.glob('submission/*.ans'):
            files.append((ans2in(ans), ans))
    else:
        if not args.ans:
            if '.ans' in args.inp:
                args.ans = args.inp
                args.inp = ans2in(args.ans)
            elif '.in' in args.inp:
                args.ans = in2ans(args.inp)
            else:
                args.inp = args.inp.replace('.max', '')
                args.ans = 'submission/' + args.inp + '.ans'
                args.inp = 'in/' + args.inp + '.in'
        files = [(args.inp, args.ans)]

    for inpf, ansf in files:
        with open(inpf, 'r') as f:
            inp = f.read()
        with open(ansf, 'r') as f:
            ans = f.read()

        print('{} {}'.format(inpf, ansf))
        print(score(inp, ans))
