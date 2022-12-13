
import os, sys, time, argparse, urllib.request, re
from datetime import datetime, timezone, timedelta

year = 2022
tz = timezone(timedelta(hours = -5), 'EST')
dirname = 'inputs'
filename_format = 'day{}.txt'
answers_filename_format = 'day{}_answers.txt'
input_url_format = 'https://adventofcode.com/{}/day/{}/input'
puzzle_url_format = 'https://adventofcode.com/{}/day/{}'

def main():
    try:
        get_inputs(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session-id', default = os.getenv('ADVENTOFCODE_SESSION'), help = 'the session id for the logged in user')
    parser.add_argument('--wait', action = 'store_true', default = False, help = 'wait for inputs to become available')
    parser.add_argument('--with-answers', action = 'store_true', default = False, help = 'also download answers')
    return parser.parse_args()

def get_inputs(args):
    make_inputs_dir()
    last_day = get_last_day()
    for day in range(1, last_day + 1):
        get_input(day, args)
        if args.with_answers:
            get_answers(day, args)
    if args.wait:
        for day in range(last_day + 1, 25 + 1):
            wait_for_input(day)
            get_input(day)

def make_inputs_dir():
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def get_last_day():
    now = datetime.now(tz)
    if now.year < year or (now.year == year and now.month < 12):
        return 0
    if now.year == year and now.month == 12 and now.day <= 25:
        return now.day
    return 25

def wait_for_input(day):
    print('Waiting on input for day', day, '...')
    while get_last_day() < day:
        time.sleep(1.0)

def get_input(day, args):
    path = os.path.join(dirname, filename_format.format(day))
    if not os.path.exists(path):
        print('Getting input for day', day)
        try:
            input = download_input(day, args)
        except urllib.HTTPError as error:
            print('Failed!!!', error.status, error.reason)
        else:
            write(path, input)
            print('Done')

def download_input(day, args):
    req = urllib.request.Request(input_url_format.format(year, day))
    req.add_header('Accept', 'text/plain')
    add_session_header(req, args)
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf8')

def get_answers(day, args):
    path = os.path.join(dirname, answers_filename_format.format(day))
    if not os.path.exists(path) or len(read_answers(path)) < total_answers(day):
        print('Getting answers for day', day)
        try:
            answers = download_answers(day, args)
        except OSError as error:
            print('Failed!!!', error)
        else:
            if len(answers) == 0:
                print('No answers found!')
            else:
                write_answers(path, answers)
                if len(answers) < total_answers(day):
                    print('Missing some answers for day', day)
                else:
                    print('Done')

def total_answers(day):
    return 1 if day == 25 else 2

def download_answers(day, args):
    req = urllib.request.Request(puzzle_url_format.format(year, day))
    req.add_header('Accept', 'text/html')
    add_session_header(req, args)
    with urllib.request.urlopen(req) as res:
        return extract_answers(res.read().decode('utf8'))

def extract_answers(html):
    return re.findall(r'Your puzzle answer was <code>(.*?)</code>', html)

def add_session_header(req, args):
    if args.session_id:
        req.add_header('Cookie', 'session=' + args.session_id)

def read_answers(path):
    return read(path).splitlines()

def write_answers(path, answers):
    write(path, '\n'.join(answers))

def read(path):
    with open(path, 'r', encoding = 'utf8') as file:
        return file.read()

def write(path, text):
    with open(path, 'w', encoding = 'utf8') as file:
        file.write(text)

if __name__ == '__main__':
    main()
