import framework

def solve(input):
    packet = input.strip()
    yield start(packet, 4)
    yield start(packet, 14)

def start(packet, marker_size):
    for i in range(marker_size, len(packet)):
        if is_marker(packet[i - marker_size : i]):
            return i
    return None

def is_marker(s):
    return len(set(s)) == len(s)

if __name__ == '__main__':
    framework.main()
