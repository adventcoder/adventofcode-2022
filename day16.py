import framework
import math
from functools import cache

def solve(input, dot_path = None):
    statements = [line.split(';') for line in input.splitlines()]

    valves = []
    rates = []
    for A, _ in statements:
        tokens = A.replace('=', ' ').split()
        valves.append(tokens[1])
        rates.append(int(tokens[-1]))

    tunnels = []
    for i, (_, B) in enumerate(statements):
        tunnels.append([math.inf] * len(valves))
        tokens = B.replace(',', '').split()
        for valve in tokens[4:]:
            tunnels[i][valves.index(valve)] = 1
        tunnels[i][i] = 0

    if dot_path is not None:
        with open(dot_path, 'w') as file:
            print('digraph {', file = file)
            for i in range(len(valves)):
                for j in range(len(valves)):
                    if i != j and tunnels[i][j] != math.inf:
                        print(valves[i], '->', valves[j], ';', file = file)
            print('}', file = file)

    # Run Floyd Warshall
    for k in range(len(valves)):
        for i in range(len(valves)):
            for j in range(len(valves)):
                if tunnels[i][j] > tunnels[i][k] + tunnels[k][j]:
                    tunnels[i][j] = tunnels[i][k] + tunnels[k][j]

    @cache
    def find_max_pressure(i, targets, time):
        max_pressure = 0
        for j in targets:
            dt = tunnels[i][j] + 1
            if dt <= time:
                pressure = rates[j] * (time - dt) + find_max_pressure(j, targets - frozenset([j]), time - dt)
                if pressure > max_pressure:
                    max_pressure = pressure
        return max_pressure

    def find_max_pressure2(start, targets, time):
        # Just loop over all ways to divide up the valves. This is super slow!
        # TODO: Maybe I'll revisit it some day (I won't)
        max_pressure = 0
        for n in range(1 << (len(targets) - 1)):
            my_targets = frozenset(x for i, x in enumerate(targets) if (n >> i) & 1 == 1)
            pressure = find_max_pressure(start, my_targets, time) + find_max_pressure(start, targets - my_targets, time)
            if pressure > max_pressure:
                max_pressure = pressure
        return max_pressure

    start = valves.index('AA')
    targets = frozenset(i for i, rate in enumerate(rates) if rate > 0)
    yield find_max_pressure(start, targets, 30)
    yield find_max_pressure2(start, targets, 26)

if __name__ == '__main__':
    framework.main()
