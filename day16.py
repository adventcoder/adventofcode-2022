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
    def find_candidate_paths(i, visited, time):
        paths = [(0, 0)]
        for j in targets:
            dt = tunnels[i][j] + 1
            if dt < time and not (visited >> j) & 1:
                for pressure, opened in find_candidate_paths(j, visited | (1 << j), time - dt):
                    paths.append((pressure + rates[j] * (time - dt), opened | (1 << j)))
        return nlargest(10, paths)

    def find_max_pressure1(start, time):
        max_pressure = 0
        for pressure, opened in find_candidate_paths(start, 0, time):
            if pressure > max_pressure:
                # print('pressure:', pressure, 'opened:', bin(opened))
                max_pressure = pressure
        return max_pressure

    def find_max_pressure2(start, time):
        max_pressure = 0
        for pressure1, opened1 in find_candidate_paths(start, 0, time):
            for pressure2, opened2 in find_candidate_paths(start, opened1, time):
                pressure = pressure1 + pressure2
                if pressure > max_pressure:
                    # print('pressure:', pressure, 'opened1:', bin(opened1), 'opened2:', bin(opened2))
                    max_pressure = pressure
        return max_pressure

    start = valves.index('AA')
    yield find_max_pressure1(start, 30)
    yield find_max_pressure2(start, 26)

if __name__ == '__main__':
    framework.main()
