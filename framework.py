
import __main__, argparse, os, sys, time, math

def main(input = None):
    args = parse_args()
    if input is None:
        input = get_input(args)
    print_answers(__main__.solve, input)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help = 'path to custom input file (use "-" for stdin)')
    return parser.parse_args()

def get_input(args, mod = __main__):
    if args.input is not None:
        if args.input == '-':
            return sys.stdin.read()
        else:
            return read_input(args.input)
    return read_input(get_input_path(mod))

def get_input_path(mod):
    name = os.path.basename(mod.__file__).replace('.py', '.txt')
    return os.path.join(os.path.dirname(mod.__file__), 'inputs', name)

def read_input(path):
    with open(path, 'r', encoding = 'utf8') as file:
        return file.read()

def print_answers(solver, input):
    start_time = time.perf_counter()
    for i, answer in enumerate(solver(input)):
        answer_time = time.perf_counter() - start_time
        print_answer(i + 1, answer, answer_time)
        start_time = time.perf_counter()

def print_answer(n, answer, answer_time):
    print('Part {}: {} [{}]'.format(n, answer, format_time(answer_time)))

def format_time(time):
    seconds = math.floor(time)
    milliseconds = (time - seconds) * 1000
    parts = []
    if seconds:
        parts.append('%d s' % seconds)
    parts.append('%.3f ms' % milliseconds)
    return ' '.join(parts)
