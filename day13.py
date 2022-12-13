import framework
from functools import cmp_to_key
from math import prod
from ast import literal_eval

def solve(input):
    pairs = [[literal_eval(line) for line in chunk.splitlines()] for chunk in input.split('\n\n')]
    yield sum(i + 1 for i, (L, R) in enumerate(pairs) if compare(L, R) < 0)

    divider_packets = [[[2]], [[6]]]
    packets = [packet for pair in pairs for packet in pair]
    packets.extend(divider_packets)
    packets.sort(key = cmp_to_key(compare))
    yield prod(i + 1 for i, packet in enumerate(packets) if packet in divider_packets)

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
