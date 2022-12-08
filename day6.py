import framework
from utils import sliding_window

def solve(input):
    packet = input.strip()
    yield start(packet, 4)
    yield start(packet, 14)

def start(packet, n):
    return next(i + n for i, marker in enumerate(sliding_window(packet, n)) if len(set(marker)) == n)

if __name__ == '__main__':
    framework.main()
