
import __main__, re, os, time, argparse

def main():
  day = get_day_number(__main__)
  print_answers(__main__.solve, get_input(day))

def get_day_number(mod):
    name = os.path.basename(mod.__file__)
    return int(re.search(r'\d+', name).group())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help = 'path to a custom input file')
    return parser.parse_args()

def print_answers(solver, input):
    start_time = time.perf_counter()
    for i, answer in enumerate(solver(input)):
        answer_time = time.perf_counter() - start_time
        print_answer(i + 1, answer, answer_time)
        start_time = time.perf_counter()

def print_answer(n, answer, answer_time):
    print('Part {}: {} [{}]'.format(n, answer, format_time(answer_time)))

def format_time(time):
    parts = []
    if time >= 1:
        parts.append('%d s' % time)
    parts.append('%.3f ms' % (time * 1000))
    return ' '.join(parts)

def get_input(day):
    with open(get_input_path(day), 'r', encoding = 'utf8') as file:
        return file.read()

def get_input_path(day):
    return 'inputs/day{}.txt'.format(day)
