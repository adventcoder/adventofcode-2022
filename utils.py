
import functools

# Basic Utils

def product(iterable):
    return functools.reduce(lambda x, y: x * y, iterable, 1)

# Common Input Parsing Utils

def read(path):
    with open(path) as file:
        return file.read()

def read_chunks(path):
    return read(path).split('\n\n')

def read_list(path, parser = str):
    return parse_list(read(path), parser)

def read_table(path, parsers = None, separator = None):
    return parse_table(read(path), parsers, separator)

def read_grid(path, parser = str):
    return parse_table(read(path), parser)

def parse_list(chunk, parser = str):
    return [parser(line.strip()) for line in chunk.splitlines()]

def parse_table(chunk, parsers = None, separator = None):
    if parsers is None:
        return parse_list(chunk, lambda line: line.split(separator))
    else:
        return parse_list(chunk, lambda line: tuple(f(x) for f, x in zip(parsers, line.split(separator, len(parsers)))))

def parse_grid(chunk, parser = str):
    return parse_list(chunk, lambda line: [parser(c) for c in line])
