
import argparse, sys, os, time, re, importlib.util
from math import floor

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
    puzzles = load_puzzles(args)
    total_stars = 0
    total_time = 0
    print("--- Advent of Code Year 2022 ---")
    print()
    for day in sorted(puzzles.keys()):
        mod, input, answers = puzzles[day]
        print("Day {}: ".format(str(day).rjust(2)), end = '', flush = True)
        stars, time = test(mod.solve, input, answers)
        if day == 25 and stars == len(answers):
            print('*', end = '')
            stars += 1
        print(" {}/{} [{}]".format(stars, len(answers) + (day == 25), format_time(time)))
        total_stars += stars
        total_time += time
    print()
    print("Total stars:", total_stars)
    print("Total time:", format_time(total_time))
    if total_stars == 50:
        print()
        print("Merry Christmas :)")

def test(solver, input, answers):
    stars = 0
    total_time = 0
    start_time = time.perf_counter()
    attempts = solver(input)
    for answer in answers:
        try:
            attempt = next(attempts)
        except StopIteration:
            print('.', end = '')
        except Exception:
            print('!', end = '')
        else:
            total_time += time.perf_counter() - start_time
            start_time = time.perf_counter()
            if str(attempt) == answer:
                print('*', end = '')
                stars += 1
            else:
                print('X', end = '')
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

def load_puzzles(args):
    puzzles = {}
    inputs_dirname = 'bigboy_inputs' if args.bigboy else 'inputs'
    for name in os.listdir('.'):
        path = os.path.join('.', name)
        if match := re.fullmatch(r'day(\d+).py', name):
            day = int(match.group(1))
            input_path = os.path.join(inputs_dirname, 'day{}.txt'.format(day))
            answers_path = os.path.join(inputs_dirname, 'day{}_answers.txt'.format(day))
            if os.path.exists(input_path) and os.path.exists(answers_path):
                mod = load_module(os.path.splitext(name)[0], path)
                input = read(input_path)
                answers = read(answers_path).splitlines()
                puzzles[day] = (mod, input, answers)
    return puzzles

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def read(path):
    with open(path, 'r', encoding = 'utf8') as file:
        return file.read()

if __name__ == '__main__':
    main()
