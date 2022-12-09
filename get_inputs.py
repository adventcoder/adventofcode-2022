
import os, sys, time, argparse, urllib.request
from datetime import datetime, timezone, timedelta

year = 2022
tz = timezone(timedelta(hours = -5), 'EST')
dirname = 'inputs'
filename_format = 'day{}.txt'
url_format = 'https://adventofcode.com/{}/day/{}/input'

def main():
    try:
        get_inputs(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session-id', default = os.getenv('ADVENTOFCODE_SESSION'), help = 'the session id for the logged in user')
    parser.add_argument('--wait', action = 'store_true', default = False, help = 'wait for inputs to become available')
    return parser.parse_args()

def get_inputs(args):
    make_inputs_dir()
    last_day = get_last_day()
    for day in range(1, last_day + 1):
        get_input(day, args)
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
    path = get_input_path(day)
    if not os.path.exists(path):
        print('Getting input for day', day)
        try:
            download_input(path, day, args)
        except OSError as error:
            print('Failed!!!', error)
            if os.path.exists(path):
                os.remove(path)
        else:
            print('Done')

def get_input_path(day):
    return os.path.join(dirname, filename_format.format(day))

def download_input(path, day, args):
    req = urllib.request.Request(url_format.format(year, day))
    add_headers(req, args)
    with urllib.request.urlopen(req) as res:
        with open(path, 'wb') as file:
            file.write(res.read())

def add_headers(req, args):
    req.add_header('Accept', 'text/plain')
    if args.session_id:
        req.add_header('Cookie', 'session=' + args.session_id)

if __name__ == '__main__':
    main()
