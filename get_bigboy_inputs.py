
import os, sys, re, json, argparse, urllib.request, py7zr

dirname = 'bigboy_inputs'
filename_format = 'day{}.txt'
contents_url = 'https://api.github.com/repos/Error916/Aoc2022/contents/bigboy_input?ref=main'
filename_pattern = r'bigboyday(\d+)\.7z'
archive_name_pattern = r'.*\.txt'

def main():
    try:
        get_bigboy_inputs(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type = parse_days, help = 'days to download')
    return parser.parse_args()

def parse_days(arg):
    if arg.strip() == '*':
        return None
    days = set()
    for token in arg.split(','):
        if '-' in token:
            first, last = map(int, token.split('-'))
            for day in range(first, last + 1):
                days.add(day)
        else:
            days.add(int(token))
    return days

def get_bigboy_inputs(args):
    make_bigboy_inputs_dir()
    urls = get_download_urls(args)
    for day in sorted(urls.keys()):
        get_bigboy_input(day, urls[day])

def make_bigboy_inputs_dir():
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def get_download_urls(args):
    urls = {}
    req = urllib.request.Request(contents_url)
    with urllib.request.urlopen(req) as res:
        for entry in json.load(res):
            match = re.fullmatch(filename_pattern, entry['name'])
            if match:
                day = int(match.group(1))
                if args.days is None or day in args.days:
                    urls[day] = entry['download_url']
    print('Found', len(urls), 'bigboy inputs to download')
    return urls

def get_bigboy_input(day, download_url):
    path = get_bigboy_input_path(day)
    if os.path.exists(path):
        print('Already downloaded bigboy input for day', day)
    else:
        print('Getting bigboy input for day', day)
        try:
            download_input(path, download_url)
        except OSError as error:
            print('Failed!!!', error)
            if os.path.exists(path):
                os.remove(path)
        else:
            print('Done')

def get_bigboy_input_path(day):
    return os.path.join(dirname, filename_format.format(day))

def download_input(path, download_url):
    archive_path = path.replace('.txt', '.7z')
    try:
        if not os.path.exists(archive_path):
            req = urllib.request.Request(download_url)
            with urllib.request.urlopen(req) as res:
                with open(archive_path, 'wb') as file:
                    copy(file, res)
        with py7zr.SevenZipFile(archive_path) as archive_file:
            names = [name for name in archive_file.getnames() if re.fullmatch(archive_name_pattern, name)]
            if names:
                archive = archive_file.read(targets = [names[0]])
                with open(path, 'wb') as file:
                    copy(file, archive[names[0]])
    finally:
        if os.path.exists(archive_path):
            os.remove(archive_path)

def copy(dest, src):
    while chunk := src.read(100 * 1024):
        dest.write(chunk)

if __name__ == '__main__':
    main()
