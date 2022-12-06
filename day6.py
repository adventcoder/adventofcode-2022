import framework

def solve(input):
    packet = input.strip()
    yield start(packet, 4)
    yield start(packet, 14)

def start(packet, n):
    # window size is too small to bother with sliding window
    for start in range(n, len(packet) + 1):
        if len(set(packet[start - n : start])) == n:
            return start
    return None

if __name__ == '__main__':
    framework.main()
