import framework
import re
from math import *
from collections import defaultdict

# TODO: this could be a bit faster maybe.
def solve(input):
    blueprints = [Blueprint(line) for line in input.splitlines()]
    yield sum(blueprint.num * astar(24, blueprint) for blueprint in blueprints)
    yield prod(astar(32, blueprint) for blueprint in blueprints[:3])

class Blueprint:
    def __init__(self, line):
        self.num, a, b, c, d, e, f = map(int, re.findall(r'\d+', line))
        self.costs = [(a, 0, 0, 0), (b, 0, 0, 0), (c, d, 0, 0), (e, 0, f, 0)]
        self.max_cost = [max(a, b, c, e), d, f]

def astar(time, blueprint):
    start = State((0, 0, 0, 0), (1, 0, 0, 0), time)
    best = {}
    best[start.key()] = start
    queue = defaultdict(list)
    max_score = start.heuristic()
    queue[max_score].append(start)
    while queue:
        curr = queue[max_score].pop()
        if not queue[max_score]:
            del queue[max_score]
            max_score = max(queue.keys()) if queue else 0
        if curr.time == 0:
            return curr.resources[3]
        for next in curr.neighbours(blueprint):
            key = next.key()
            if key not in best or next.resources[3] > best[key].resources[3]:
                best[key] = next
                score = next.heuristic()
                queue[score].append(next)
                max_score = max(score, max_score)

class State:
    def __init__(self, resources, robots, time):
        self.resources = resources
        self.robots = robots
        self.time = time

    def key(self):
        return (self.resources[:3], self.robots, self.time)

    def heuristic(self):
        return self.resources[3] + self.robots[3] * self.time + self.time*(self.time-1)//2

    def neighbours(self, blueprint):
        bought_any = False
        for i in range(4):
            if self.worth_buying(blueprint, i):
                time = self.time_to_wait(blueprint, i)
                if time + 1 < self.time:
                    yield self.wait_then_buy(blueprint, i, time)
                    bought_any = True
        if not bought_any:
            yield self.wait()

    def worth_buying(self, blueprint, i):
        return i == 3 or self.resources[i] + self.robots[i] * self.time < blueprint.max_cost[i] * self.time

    def time_to_wait(self, blueprint, i):
        max_time = 0
        for j in range(4):
            if self.resources[j] < blueprint.costs[i][j]:
                if self.robots[j] == 0:
                    return inf
                time = ceil((blueprint.costs[i][j] - self.resources[j]) / self.robots[j])
                max_time = max(time, max_time)
        return max_time

    def wait(self):
        return State(tuple(self.resources[j] + self.robots[j] * self.time for j in range(4)), self.robots, 0)

    def wait_then_buy(self, blueprint, i, time):
        return State(tuple(self.resources[j] + self.robots[j] * (time + 1) - blueprint.costs[i][j] for j in range(4)),
                    tuple(self.robots[j] + (i == j) for j in range(4)),
                    self.time - time - 1)

if __name__ == '__main__':
    framework.main()
