import framework
from utils import sliding_window

def solve(input):
    packet = input.strip()
    yield start(packet, 4)
    yield start(packet, 14)

def start(packet, marker_size):
    for i, window in enumerate(sliding_window(packet, marker_size)):
        if is_marker(window):
            return i + marker_size
    return None

def is_marker(window):
    return len(set(window)) == len(window)

if __name__ == '__main__':
    framework.main()
