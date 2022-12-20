import framework

# TODO: slow, tried linked list and it was slower
def solve(input):
    vals = [int(line) for line in input.splitlines()]
    yield sum(coords(mix(vals)))
    yield sum(coords(mix([val * 811589153 for val in vals], 10)))

def coords(vals):
    i = vals.index(0)
    return (vals[(i + n) % len(vals)] for n in (1000, 2000, 3000))

def mix(vals, reps = 1):
    indexes = list(range(len(vals)))
    for _ in range(reps):
        for index in range(len(vals)):
            move(indexes, indexes.index(index), vals[index])
    return [vals[index] for index in indexes]

def move(vals, i, n):
    val = vals.pop(i)
    vals.insert((i + n) % len(vals), val)

if __name__ == '__main__':
    framework.main()
