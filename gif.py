
import struct
from contextlib import contextmanager

# Data Types

class ScreenDescriptor:
    def __init__(self, width, height, colors = None):
        self.width = width
        self.height = height
        self.colors = colors
        self.background_color_index = 0
        self.aspect_ratio = None
        self.color_resolution = 8

class Image:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = bytearray(width * height)
        self.colors = None

    def get_pixel(self, x, y):
        self.data[x + self.width * y]

    def set_pixel(self, x, y, color_index):
        self.data[x + self.width * y] = color_index

# High Level IO

@contextmanager
def open_graphics(path, screen_descriptor, loop_count = None):
    with open(path, 'wb') as io:
        writer = Writer(io)
        writer.write_header()
        writer.write_screen_descriptor(screen_descriptor)
        writer.write_netscape_app_ext(loop_count)
        yield GraphicsOutput(writer)
        writer.write_footer()

class GraphicsOutput:
    def __init__(self, writer):
        self.writer = writer

    def comment(self, comment):
        self.writer.write_comment_ext(comment)

    def render(self, image, delay = None, transparent_color_index = None):
        if delay is not None or transparent_color_index is not None:
            self.writer.write_graphic_control_ext(delay, transparent_color_index)
        self.writer.write_image(image)

# Low Level IO

class Writer:
    def __init__(self, io):
        self.io = io

    def write_header(self):
        self.write_bytes(b'GIF89a')

    def write_screen_descriptor(self, screen):
        self.write_bytes(struct.pack(b'<HHBBB',
            screen.width,
            screen.height,
            pack_bits((1, 3, 1 ,3), (
                1 if screen.colors else 0,
                screen.color_resolution - 1,
                0,
                color_table_depth(screen.colors) - 1 if screen.colors else 0
            )),
            screen.background_color_index,
            0 if screen.aspect_ratio is None else int(screen.aspect_ratio * 64) - 15
        ))
        if screen.colors:
            self.write_bytes(pack_color_table(screen.colors))

    def write_image(self, image):
        self.write_image_descriptor(image)
        self.write_image_data(image)

    def write_image_descriptor(self, image):
        self.write_bytes(b',')
        self.write_bytes(struct.pack(b'<HHHHB',
            image.x,
            image.y,
            image.width,
            image.height,
            pack_bits((1, 1, 1, 2, 3), (
                1 if image.colors else 0,
                0,
                0,
                0,
                color_table_depth(image.colors) - 1 if image.colors else 0
            ))
        ))
        if image.colors:
            self.write_bytes(pack_color_table(image.colors))

    def write_image_data(self, image):
        max_color_index = max(image.data)
        min_code_size = 2
        while max_color_index >= (1 << min_code_size):
            min_code_size += 1
        self.write_byte(min_code_size)
        self.write_data(compress(image.data, min_code_size))

    def write_graphic_control_ext(self, delay, transparent_color_index):
        self.write_bytes(b'!')
        self.write_byte(0xF9)
        self.write_subblock(struct.pack('<BHB',
            0 if transparent_color_index is None else 1,
            0 if delay is None else int(delay * 100),
            0 if transparent_color_index is None else transparent_color_index
        ))
        self.write_byte(0)

    def write_comment_ext(self, comment):
        self.write_bytes(b'!')
        self.write_byte(0xFE)
        self.write_data(comment.encode('ascii'))

    def write_app_ext(self, app_id, auth_code, subblocks):
        self.write_bytes(b'!')
        self.write_byte(0xFF)
        self.write_subblock(app_id + auth_code)
        for subblock in subblocks:
            self.write_subblock(subblock)
        self.write_byte(0)

    def write_netscape_app_ext(self, loop_count = None, buffer_size = None):
        subblocks = []
        if loop_count is not None:
            subblocks.append(struct.pack('<BH', 1, loop_count))
        if buffer_size is not None:
            subblocks.append(struct.pack('<BL', 2, buffer_size))
        if subblocks:
            self.write_app_ext(b'NETSCAPE', b'2.0', subblocks)

    def write_footer(self):
        self.write_bytes(b';')

    def write_data(self, data):
        for i in range(0, len(data), 255):
            self.write_subblock(data[i : i + 255])
        self.write_byte(0)

    def write_subblock(self, subblock):
        self.write_byte(len(subblock))
        self.write_bytes(subblock)

    def write_byte(self, b):
        self.write_bytes(bytes([b]))

    def write_bytes(self, b):
        self.io.write(b)

# Helper Functions

def pack_bits(sizes, values):
    bits = 0
    offset = sum(sizes)
    for size, value in zip(sizes, values):
        max_value = (1 << size) - 1
        if not 0 <= value <= max_value:
            raise ValueError('value {} out of range 0 <= value <= {}', value, max_value)
        offset -= size
        bits |= value << offset
    return bits

def color_table_depth(colors):
    depth = 1
    while (1 << depth) < len(colors):
        depth += 1
    return depth

def pack_color_table(colors):
    size = 1 << color_table_depth(colors)
    data = bytearray(size * 3)
    i = 0
    for color in colors:
        data[i] = (color >> 16) & 0xFF
        data[i + 1] = (color >> 8) & 0xFF
        data[i + 2] = color & 0xFF
        i += 3
    return data

# Compression

def compress(data, min_code_size):
    compressor = Compressor(min_code_size)
    compressor.append(data)
    compressor.stop()
    return compressor.output

class Compressor:
    @property
    def clear_code(self):
        return 1 << self.min_code_size

    @property
    def stop_code(self):
        return self.clear_code + 1

    def __init__(self, min_code_size, max_code_size = 12):
        self.min_code_size = min_code_size
        self.max_code_size = max_code_size
        self.output = bytearray()
        self.bits = 0
        self.bit_size = 0
        self.seq = bytes()
        self.clear()

    def clear(self):
        self.dict = {}
        for i in range(self.clear_code):
            self.dict[bytes([i])] = i
        self.next_code = self.clear_code + 2
        self.code_size = self.min_code_size + 1
        self.write_code(self.clear_code)

    def append(self, data):
        for b in data:
            new_seq = self.seq + bytes([b])
            if new_seq in self.dict:
                self.seq = new_seq
            else:
                self.write_code(self.dict[self.seq])
                self.assign_code(new_seq)
                self.seq = bytes([b])

    def stop(self):
        if self.seq:
            self.write_code(self.dict[self.seq])
            self.seq = bytes()
        self.write_code(self.stop_code)
        self.flush_bits()

    def assign_code(self, seq):
        # code_size corresponds to the maximum code currently in the dict.
        # since we're now adding next_code check it to see if we need to extend the code size.
        # clear if the max code size has already been reached.
        if self.next_code == (1 << self.code_size):
            if self.code_size == self.max_code_size:
                self.clear()
            else:
                self.code_size += 1
        self.dict[seq] = self.next_code
        self.next_code += 1

    def write_code(self, code):
        self.bits |= (code << self.bit_size)
        self.bit_size += self.code_size
        while self.bit_size >= 8:
            self.output.append(self.bits & 0xFF)
            self.bits >>= 8
            self.bit_size -= 8

    def flush_bits(self):
        if self.bit_size > 0:
            self.output.append(self.bits)
            self.bits = 0
            self.bit_size = 0
