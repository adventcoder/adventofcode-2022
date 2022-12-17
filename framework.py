
import __main__, argparse, os, sys, time, ast, re
from math import floor

def main(input = None):
    args = parse_args()
    if input is None:
        input = get_input(get_day_number(__main__), args)
    print_answers(__main__.solve, input, **get_solver_args(args))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help = 'path to custom input file (use "-" for stdin)')
    parser.add_argument('--bigboy', action = 'store_true', default = False, help = 'use bigboy input instead of normal input')
    parser.add_argument('--solver-arg', dest = 'solver_args', default = [], action = 'append', metavar='KEY=VALUE')
    return parser.parse_args()

def get_day_number(mod):
    return int(re.match(r'day(\d+)', os.path.basename(mod.__file__)).group(1))

def get_input(day, args):
    if args.input is not None:
        if args.input == '-':
            return sys.stdin.read()
        else:
            return read(args.input)
    return read(get_input_path(day, args))

def get_input_path(day, args):
    dirname = 'bigboy_inputs' if args.bigboy else 'inputs'
    return os.path.join(dirname, 'day{}.txt'.format(day))

def get_solver_args(args):
    kwargs = {}
    for str in args.solver_args:
        key, value = str.split('=', 2)
        kwargs[key] = ast.literal_eval(value)
    return kwargs

def print_answers(solver, input, **kwargs):
    start_time = time.perf_counter()
    for i, answer in enumerate(solver(input, **kwargs)):
        answer_time = time.perf_counter() - start_time
        print_answer(i + 1, answer, answer_time)
        start_time = time.perf_counter()

def print_answer(n, answer, answer_time):
    label = 'Part {}:'.format(n)
    lines = str(answer).splitlines()
    for i, line in enumerate(lines):
        prefix = label if i == 0 else ' ' * len(label)
        suffix = '[' + format_time(answer_time) + ']' if i == len(lines) - 1 else ''
        print(prefix, line, suffix)

def format_time(time):
    seconds = floor(time)
    milliseconds = (time - seconds) * 1000
    parts = []
    if seconds:
        parts.append('%d s' % seconds)
    parts.append('%.3f ms' % milliseconds)
    return ' '.join(parts)

def read(path):
    with open(path, 'r', encoding = 'utf8') as file:
        return file.read()
