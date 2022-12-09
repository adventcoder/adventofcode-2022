import framework

def solve(input):
    packet = input.strip()
    yield end_of_marker(packet, 4)
    yield end_of_marker(packet, 14)

def end_of_marker(packet, size):
    for end in range(size, len(packet) + 1):
        if is_marker(packet[end - size : end]):
            return end
    return None

def is_marker(slice):
    return len(set(slice)) == len(slice)

if __name__ == '__main__':
    framework.main()
