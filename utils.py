
import functools

# Basic Utils

def product(xs):
    return functools.reduce(lambda x, y: x * y, xs, 1)

# Common Input Parsing Utils

def read(path):
    with open(path) as file:
        return file.read()

def read_chunks(path):
    return read(path).split('\n\n')

def read_list(path, parser = str):
    return parse_list(read(path), parser)

def read_table(path, parsers = None):
    return parse_table(read(path), parsers)

def read_grid(path, parser = str):
    return parse_table(read(path), parser)

def parse_list(chunk, parser = str):
    return [parser(line.strip()) for line in chunk.splitlines()]

def parse_table(chunk, parsers = None):
    if parsers is None:
        return parse_list(chunk, str.split)
    else:
        return parse_list(chunk, lambda line: tuple(f(x) for f, x in zip(parsers, line.split())))

def parse_grid(chunk, parser = str):
    return parse_list(chunk, lambda line: [parser(c) for c in line])
