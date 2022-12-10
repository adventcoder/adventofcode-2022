
import functools

# Basic Utils

def sgn(x):
    return (x > 0) - (x < 0)

def groups(seq, size):
    return (seq[i : i + size] for i in range(0, len(seq), size))

def product(iterable):
    return functools.reduce(lambda x, y: x * y, iterable, 1)

# Common Input Parsing Utils

def parse_list(chunk, parser = str):
    return [parser(line.strip()) for line in chunk.splitlines()]

def parse_table(chunk, parsers = None, separator = None):
    if parsers is None:
        return parse_list(chunk, lambda line: line.split(separator))
    else:
        return parse_list(chunk, lambda line: tuple(f(x) for f, x in zip(parsers, line.split(separator, len(parsers)))))

def parse_grid(chunk, parser = str):
    return parse_list(chunk, lambda line: [parser(c) for c in line])
