
import importlib, argparse, os, time, re
from itertools import islice
from math import floor

inputs_dirname = 'inputs'
input_name_pattern = r'day(\d+).txt'
answers_name_pattern = r'day(\d+)_answers.txt'

def main():
    scoresheet(parse_args())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bigboy', action = 'store_true', default = False, help = 'use bigboy inputs instead of normal inputs')
    return parser.parse_args()

def scoresheet(args):
    print("--- Advent of Code Year 2022 ---")
    print()
    total_stars = 0
    total_time = 0
    for day, input, answers in get_inputs_with_answers(args):
        mod = importlib.import_module('day{}'.format(day))
        stars, time = exec(mod.solve, input, answers)
        print("Day {}: {} [{}]".format(str(day).rjust(2), (stars * '*').ljust(2), format_time(time)))
        total_stars += stars
        total_time += time
    print()
    print("Total stars:", total_stars)
    print("Total time:", format_time(total_time))

def exec(solver, input, answers):
    start_time = time.perf_counter()
    attempts = list(islice(solver(input), len(answers)))
    end_time = time.perf_counter()
    return sum(str(attempt) == answer for attempt, answer in zip(attempts, answers)), end_time - start_time

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

def get_inputs_with_answers(args):
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
