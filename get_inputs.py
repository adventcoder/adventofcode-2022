
import os, sys, time
import argparse
from datetime import datetime, timezone, timedelta
import urllib.request, urllib.error

year = 2022
tz = timezone(timedelta(hours = -5), 'EST')
dirname = 'inputs'
filename_format = 'day{}.txt'
url_format = 'https://adventofcode.com/{}/day/{}/input'
encoding = 'utf-8'

def main():
    try:
        get_inputs(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session-id', help = 'the session id for the logged in user')
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
            text = read_input(day, args)
            with open(path, 'w') as file:
                file.write(text)
            print('Done')
        except urllib.error.HTTPError as error:
            print('Failed!!! Reason:', error.code, error.reason)
            # TODO: retry on server error/timeout?

def get_input_path(day):
    return os.path.join(dirname, filename_format.format(day))

def read_input(day, args):
    url = url_format.format(year, day)
    req = urllib.request.Request(url)
    session_id = get_session_id(args)
    if session_id is not None:
        req.add_header('Cookie', 'session=' + session_id)
    with urllib.request.urlopen(req) as res:
        return res.read().decode(encoding)

def get_session_id(args):
    if args.session_id is not None:
        return args.session_id
    # add this to your environment variables/bash_profile/zhsrc/wherever so you don't need to keep passing the arg.
    return os.getenv('ADVENTOFCODE_SESSION')

if __name__ == '__main__':
    main()
