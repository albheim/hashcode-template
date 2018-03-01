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
    return albin_solve(seed, inp, log)


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

    rides = ns.customers

    lines = out.split('\n')
    cars = [list(map(int, lines[i].split()[1:])) for i in range(len(lines))]

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

def albin_solve(seed, inp, log):
    ns = parse(inp)

    rides = ns.customers
    time = [0 for _ in range(ns.F)]
    pos = [(0, 0) for _ in range(ns.F)]
    ride_list = [[] for _ in range(ns.F)]

    for i, ride in enumerate(rides):
        ride.idx = i

    for t in range(ns.T):
        # print("time", t)
        for i in range(ns.F):
            # print("car", i)
            if t == time[i]:
                # pick next ride
                x, y = pos[i]
                best = -1
                bscore = -10000000000000
                btime = 0
                for r in range(len(rides)):
                    dist = abs(x - rides[r].a) + abs(y - rides[r].b)
                    dist2 = abs(rides[r].x - rides[r].a) + abs(rides[r].y - rides[r].b)
                    wait_time = max(0, rides[r].s - t - dist)
                    tot_time = t + dist + dist2 + wait_time
                    tot_score = dist2 - dist / 2.0 - wait_time / 3.5
                    if t + dist <= rides[r].s:
                        tot_score += 10 * ns.B
                    # if not possible to complete in time skip
                    if tot_time > rides[r].f or tot_time > ns.T:
                        continue
                    # if bonus, take
                    if tot_score > bscore:
                        bscore = tot_score
                        best = r
                        btime = tot_time

                # do ride best add points bscore add time
                if best != -1:
                    # print("taking customer", rides[best].idx)
                    pos[i] = (rides[best].x, rides[best].y)
                    time[i] = btime
                    ride_list[i].append(rides[best].idx)
                    del rides[best]

    result = ""
    for vehicle in ride_list:
        result += "%s " % str(len(vehicle))
        for c in vehicle:
            result += "%s " % str(c)
        result += "\n"

    return result[:-1]

def david_solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    vehicles = []
    scheduled = []
    for i in range(len(ns.customers)):
        scheduled.append(False)

    for i in range(ns.F):
        vehicle = argparse.Namespace(x=0, y=0, time=0, customers=[])
        vehicles.append(vehicle)
        for idx, customer in enumerate(ns.customers):
            to_customer = manhattan(vehicle.x, vehicle.y, customer.a, customer.b)
            start = max(vehicle.time + to_customer, customer.s)
            finish = start + trip_dist(customer)
            if not scheduled[idx] and finish <= customer.f:
                vehicle.customers.append(idx)
                scheduled[idx] = True
                vehicle.time = finish
                vehicle.x = customer.x
                vehicle.y = customer.y

    result = ""
    for vehicle in vehicles:
        result += "%s " % str(len(vehicle.customers))
        for c in vehicle.customers:
            result += "%s " % str(c)
        result += "\n"

    result = result[:-1]
    return result

def trip_dist(customer):
    return manhattan(customer.a, customer.b, customer.x, customer.y)

def manhattan(a, b, x, y):
    return abs(a - x) + abs(b - y)


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
