import framework

def solve(input):
    walls = parse_walls(input)
    max_y = max(y for _, y in walls)
    floor_y = max_y + 2
    yield len(fill(walls, 500, 0, floor_y, max_y))
    yield len(fill(walls, 500, 0, floor_y, floor_y))

def parse_walls(input):
    walls = set()
    for line in input.splitlines():
        coords = [parse_coord(s) for s in line.split('->')]
        for i in range(len(coords) - 1):
            (x0, y0), (x1, y1) = coords[i : i + 2]
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    walls.add((x, y))
    return walls

def parse_coord(s):
    return tuple(map(int, s.split(',')))

def fill(walls, start_x, start_y, floor_y, max_y):
    sand = set()
    path = []
    pos = (start_x, start_y)
    while pos and pos[1] < max_y:
        for dx in (0, -1, 1):
            new_pos = (pos[0] + dx, pos[1] + 1)
            if new_pos not in walls and new_pos not in sand and new_pos[1] < floor_y:
                path.append(pos)
                pos = new_pos
                break
        else:
            sand.add(pos)
            pos = path.pop() if path else None
    return sand

if __name__ == '__main__':
    framework.main()
