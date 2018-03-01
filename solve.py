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
    out = [[0, 1], [0, 1, 2]]

    result = ""
    for vehicle in out:
        result += "%s " % str(len(vehicle))
        for r in vehicle:
            result += "%s " % str(r)
        result += "\n"

    result = result[:-1]
    print(result)

def score(inp, out):
    ns = parse(inp)



    return 0


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
