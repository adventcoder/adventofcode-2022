
import __main__, re, os, time

def main(input = None):
  if input is None:
      input = get_input(__main__)
  print_answers(__main__.solve, input)

def get_input(mod):
    return read_input(get_day_number(mod))

def get_day_number(mod):
    name = os.path.basename(mod.__file__)
    return int(re.search(r'\d+', name).group())

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

def read_input(day):
    with open('inputs/day{}.txt'.format(day), 'r', encoding = 'utf8') as file:
        return file.read()
