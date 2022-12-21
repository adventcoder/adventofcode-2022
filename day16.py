import framework
import math
from functools import cache
from heapq import nlargest

def solve(input):
    statements = [line.split(';') for line in input.splitlines()]

    valves = []
    rates = []
    for statement1, _ in statements:
        tokens = statement1.replace('=', ' ').split()
        valves.append(tokens[1])
        rates.append(int(tokens[-1]))

    tunnels = []
    for i, (_, statement2) in enumerate(statements):
        tunnels.append([math.inf] * len(valves))
        tokens = statement2.replace(',', '').split()
        for valve in tokens[4:]:
            tunnels[i][valves.index(valve)] = 1
        tunnels[i][i] = 0

    # Run Floyd Warshall
    for k in range(len(valves)):
        for i in range(len(valves)):
            for j in range(len(valves)):
                if tunnels[i][j] > tunnels[i][k] + tunnels[k][j]:
                    tunnels[i][j] = tunnels[i][k] + tunnels[k][j]

    # only worth opening valves that will increase pressure flow
    targets = [i for i, rate in enumerate(rates) if rate > 0]

    @cache
    def find_best_path(i, time, visited = 0):
        max_pressure = 0
        for j in targets:
            dt = tunnels[i][j] + 1
            if dt < time and not (visited >> j) & 1:
                pressure = rates[j] * (time - dt) + find_best_path(j, time - dt, visited | (1 << j))
                max_pressure = max(pressure, max_pressure)
        return max_pressure

    def find_best_path2(i, time):
        max_pressure = 0
        for size in range(len(targets) // 2):
            for path, pressure in find_all_paths(i, time, size):
                max_pressure = max(pressure + find_best_path(i, time, path), max_pressure)
        return max_pressure

    @cache
    def find_all_paths(i, time, size, visited = 0):
        if size == 0:
            yield 0, 0
        else:
            for j in targets:
                dt = tunnels[i][j] + 1
                if dt < time and not (visited >> j) & 1:
                    for path, pressure in find_all_paths(j, time - dt, size - 1, visited | (1 << j)):
                        yield path | (1 << j), pressure + rates[j] * (time - dt)

    # TODO: This is not great and super slow.
    start = valves.index('AA')
    yield find_best_path(start, 30)
    yield find_best_path2(start, 26)

if __name__ == '__main__':
    framework.main()
