
import framework

def solve(input):
    droplet = set(tuple(map(int, line.split(','))) for line in input.splitlines())
    yield surface_area_approx(droplet)
    yield surface_area(droplet)

def surface_area_approx(droplet):
    area = 0
    for p in droplet:
        for n in neighbours(p):
            if n not in droplet:
                area += 1
    return area

def surface_area(droplet):
    lower = tuple(min(p[i] - 1 for p in droplet) for i in range(3))
    upper = tuple(max(p[i] + 1 for p in droplet) for i in range(3))
    outside = set([lower])
    queue = [lower]
    while queue:
        p = queue.pop()
        for n in neighbours(p):
            if n not in outside and n not in droplet and all(lower[i] <= p[i] <= upper[i] for i in range(3)):
                outside.add(n)
                queue.append(n)

    area = 0
    for p in droplet:
        for n in neighbours(p):
            if n in outside:
                area += 1
    return area

def neighbours(p):
    x, y, z = p
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y - 1, z)
    yield (x, y + 1, z)
    yield (x, y, z - 1)
    yield (x, y, z + 1)

if __name__ == '__main__':
    framework.main()
