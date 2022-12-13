import framework
from ast import literal_eval

def solve(input):
    pairs = [[literal_eval(line) for line in chunk.splitlines()] for chunk in input.split('\n\n')]
    yield sum(i + 1 for i, (L, R) in enumerate(pairs) if compare(L, R) < 0)

    i = sum(compare(packet, [[2]]) < 0 for pair in pairs for packet in pair)
    j = sum(compare(packet, [[6]]) < 0 for pair in pairs for packet in pair)
    yield (i + 1) * (j + 2)

def compare(L, R):
    if isinstance(L, int) and isinstance(R, int):
        return L - R
    elif isinstance(L, int):
        return compare([L], R)
    elif isinstance(R, int):
        return compare(L, [R])
    else:
        for x, y in zip(L, R):
            ret = compare(x, y)
            if ret != 0:
                return ret
        return len(L) - len(R)

if __name__ == '__main__':
    framework.main()
