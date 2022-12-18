import framework

def solve(input):
    jets = input.strip()
    yield height_slow(jets, 2022)
    yield height_fast(jets, 1000000000000)

def height_slow(jets, n):
    chamber = Chamber(jets)
    for _ in range(n):
        chamber.drop()
    return chamber.height

def height_fast(jets, n):
    chamber = Chamber(jets)
    seen = {}
    drops = 0
    heights = [0]
    for _ in range(n):
        key = (chamber.rock_index, chamber.jet_index, *chamber.surface())
        if key in seen:
            prev_drops = seen[key]
            q, r = divmod(n - prev_drops, drops - prev_drops)
            return heights[r + prev_drops] + (heights[drops] - heights[prev_drops]) * q
        seen[key] = drops
        chamber.drop()
        drops += 1
        heights.append(chamber.height)

class Chamber:
    rocks = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ]

    width = 7

    def __init__(self, jets):
        self.jets = jets
        self.occupied = set()
        self.heights = [0] * self.width
        self.height = 0
        self.rock_index = 0
        self.jet_index = 0

    def next_jet(self):
        jet = self.jets[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(self.jets)
        return jet

    def next_rock(self):
        rock = self.rocks[self.rock_index]
        self.rock_index = (self.rock_index + 1) % len(self.rocks)
        return rock

    def surface(self):
        return (self.height - height for height in self.heights)

    def can_place(self, rock, x, y):
        return all(0 <= x + dx < self.width and y + dy >= 0 and (x + dx, y + dy) not in self.occupied for dx, dy in rock)

    def place(self, rock, x, y):
        for dx, dy in rock:
            self.occupied.add((x + dx, y + dy))
            self.heights[x + dx] = max(self.heights[x + dx], y + dy + 1)
        self.height = max(self.heights)

    def drop(self):
        rock = self.next_rock()
        x = 2
        y = self.height + 3
        while True:
            dx = { '<': -1, '>': 1 }[self.next_jet()]
            if self.can_place(rock, x + dx, y):
                x += dx
            if self.can_place(rock, x, y - 1):
                y -= 1
            else:
                break
        self.place(rock, x, y)

    def print(self):
        for y in reversed(range(self.height)):
            print('|' + ''.join(['#' if (x, y) in self.occupied else '.' for x in range(0, self.width)]) + '|')
        print('+' + ('-' * self.width) + '+')

if __name__ == '__main__':
    framework.main()
