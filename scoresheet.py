
import importlib, argparse, sys, os, time, re
from math import floor

inputs_dirname = 'inputs'
input_name_pattern = r'day(\d+).txt'
answers_name_pattern = r'day(\d+)_answers.txt'

def main():
    try:
        scoresheet(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bigboy', action = 'store_true', default = False, help = 'use bigboy inputs instead of normal inputs')
    return parser.parse_args()

def scoresheet(args):
    print("--- Advent of Code Year 2022 ---")
    print()
    total_stars = 0
    total_time = 0
    for day, input, answers in get_test_data(args):
        mod = importlib.import_module('day{}'.format(day))
        print("Day {}: ".format(str(day).rjust(2)), end = '', flush = True)
        stars, time = test(mod.solve, input, answers)
        print(" {}/{} [{}]".format(stars, len(answers), format_time(time)))
        total_stars += stars
        total_time += time
    print()
    print("Total stars:", total_stars)
    print("Total time:", format_time(total_time))

def test(solver, input, answers):
    stars = 0
    total_time = 0
    start_time = time.perf_counter()
    attempts = solver(input)
    for answer in answers:
        try:
            attempt = next(attempts)
        except StopIteration:
            print('~', end = '', flush = True)
        except Exception:
            print('!', end = '', flush = True)
        else:
            total_time += time.perf_counter() - start_time
            start_time = time.perf_counter()
            if attempt is not None and str(attempt) == answer:
                print('*', end = '', flush = True)
                stars += 1
            else:
                print('X', end = '', flush = True)
    return stars, total_time

def format_time(time):
    minutes, seconds = divmod(floor(time), 60)
    milliseconds = (time - floor(time)) * 1000
    parts = []
    if minutes:
        parts.append('%d m' % minutes)
    if seconds:
        parts.append('%d s' % seconds)
    parts.append('%.3f ms' % milliseconds)
    return ' '.join(parts)

def get_test_data(args):
    input_paths = {}
    answers_paths = {}
    if args.bigboy:
        raise NotImplementedError()
    else:
        for name in os.listdir(inputs_dirname):
            path = os.path.join(inputs_dirname, name)
            if match := re.fullmatch(input_name_pattern, name):
                input_paths[int(match.group(1))] = path
            elif match := re.fullmatch(answers_name_pattern, name):
                answers_paths[int(match.group(1))] = path
    data = []
    for day in sorted(input_paths.keys() & answers_paths.keys()):
        input = read(input_paths[day])
        answers = read(answers_paths[day]).splitlines()
        data.append((day, input, answers))
    return data

def read(path):
    with open(path, 'r', encoding = 'utf8') as file:
        return file.read()

if __name__ == '__main__':
    main()
