import framework

def solve(input):
    packet = input.strip()
    yield start(packet, 4)
    yield start(packet, 14)

def start(packet, n):
    counts = {}
    for i in range(len(packet)):
        if i >= n:
            dec(counts, packet[i - n])
        inc(counts, packet[i])
        if len(counts) == n:
            return i + 1
    return None

def inc(counts, c):
    counts[c] = counts.get(c, 0) + 1

def dec(counts, c):
    counts[c] -= 1
    if counts[c] == 0:
        del counts[c]

if __name__ == '__main__':
    framework.main()
