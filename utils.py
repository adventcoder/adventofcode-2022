# Basic Utils

def sgn(x):
    return (x > 0) - (x < 0)

def groups(seq, size):
    return (seq[i : i + size] for i in range(0, len(seq), size))

# Common Input Parsing Utils

def parse_list(chunk, parser = str):
    return [parser(line.strip()) for line in chunk.splitlines()]

def parse_grid(chunk, parser = str):
    return [[parser(c) for c in line] for line in chunk.splitlines()]

def parse_table(chunk, parsers, separator = None):
    return [parse_tuple(line, parsers, separator) for line in chunk.splitlines()]

def parse_tuple(line, parsers, separator = None):
    return tuple(f(x) for f, x in zip(parsers, line.split(separator)))

# "OCR" (this code was written while drunk)

def ocr(grid, font, spacing = 1, x = 0, y = 0, width = None, height = None):
    if width is None:
        width = min(map(len, grid))
    if height is None:
        height = len(grid)
    letter_width, letter_height, dict = font
    cell_width = letter_width + spacing
    return ''.join(dict[pack_letter(grid, cell_x, y, letter_width, letter_height)] for cell_x in range(x, width, cell_width))

def read_font(path, spacing = 1):
    with open(path, 'r', encoding = 'utf8') as file:
        return parse_font(file.read(), spacing)

def parse_font(input, spacing = 1):
    chunks = input.split('\n\n')
    letters = chunks[0]
    grid = parse_grid(chunks[1])
    width = min(map(len, grid))
    cell_width = width // len(letters)
    letter_width = cell_width - spacing
    letter_height = len(grid)
    dict = {pack_letter(grid, i * cell_width, 0, letter_width, letter_height) : letter for i, letter in enumerate(letters)}
    return (letter_width, letter_height, dict)

def pack_letter(grid, cell_x, cell_y, width, height):
    bits = 0
    for y in range(height):
        for x in range(width):
            bits = (bits << 1) | (grid[cell_y + y][cell_x + x] == '#')
    return bits
