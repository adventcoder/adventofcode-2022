import framework

def solve(input):
    packet = input.strip()
    yield end_of_marker(packet, 4)
    yield end_of_marker(packet, 14)

def end_of_marker(packet, size):
    bitset = 0
    for i in range(len(packet)):
        if i >= size:
            bitset ^= 1 << (ord(packet[i - size]) - ord('a'))
        bitset ^= 1 << (ord(packet[i]) - ord('a'))
        if bitset.bit_count() == size:
            return i + 1
    return None

if __name__ == '__main__':
    framework.main()
