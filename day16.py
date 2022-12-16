import framework
import math
from functools import cache
from itertools import combinations

def solve(input):
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

    # Run Floyd Warshall
    for k in range(len(valves)):
        for i in range(len(valves)):
            for j in range(len(valves)):
                if tunnels[i][j] > tunnels[i][k] + tunnels[k][j]:
                    tunnels[i][j] = tunnels[i][k] + tunnels[k][j]

    targets = [i for i, rate in enumerate(rates) if rate > 0]

    @cache
    def find_max_pressure(i, time, opened = 0):
        max_pressure = 0
        for j in targets:
            dt = tunnels[i][j] + 1
            if (opened >> j) & 1 == 0 and dt <= time:
                pressure = rates[j] * (time - dt) + find_max_pressure(j, time - dt, opened | (1 << j))
                if pressure > max_pressure:
                    max_pressure = pressure
        return max_pressure

    def find_max_pressure2(start, time):
        # Just loop over all ways to divide up the valves. This is super slow!
        # TODO: Maybe I'll revisit it some day (I won't)
        max_pressure = 0
        for n in range(len(targets) // 2 + 1):
            for subset in combinations(targets, n):
                opened = 0
                for i in subset:
                    opened |= 1 << i
                pressure = find_max_pressure(start, time, opened) + find_max_pressure(start, time, ~opened)
                if pressure > max_pressure:
                    max_pressure = pressure
        return max_pressure

    yield find_max_pressure(valves.index('AA'), 30)
    yield find_max_pressure2(valves.index('AA'), 26)

if __name__ == '__main__':
    framework.main()
