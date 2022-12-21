import framework

# TODO: slow, naive delete/insert was a bit faster
def solve(input):
    vals = [int(line) for line in input.splitlines()]
    yield sum(decrypt(vals))
    yield sum(decrypt(vals, 811589153, 10))

def decrypt(vals, key = 1, reps = 1):
    prev = [(i - 1) % len(vals) for i in range(len(vals))]
    next = [(i + 1) % len(vals) for i in range(len(vals))]
    for _ in range(reps):
        for i, val in enumerate(vals):
            move(prev, next, i, val * key, len(vals))
    coords = []
    i = vals.index(0)
    for _ in range(3):
        i = go(i, next, 1000)
        coords.append(vals[i] * key)
    return coords

def move(prev, next, i, n, m):
    prev[next[i]] = prev[i]
    next[prev[i]] = next[i]
    n %= (m - 1)
    if n <= m - 1 - n:
        prev[i] = go(prev[i], next, n)
    else:
        prev[i] = go(prev[i], prev, m - 1 - n)
    next[i] = next[prev[i]]
    prev[next[i]] = i
    next[prev[i]] = i

def go(i, next, n):
    q, r = divmod(n, 8)
    for _ in range(q):
        i = next[next[next[next[next[next[next[next[i]]]]]]]]
    for _ in range(r):
        i = next[i]
    return i

if __name__ == '__main__':
    framework.main()
