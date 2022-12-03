
from utils import read_chunks, parse_list

def main():
    totals = sorted(map(parse_total, read_chunks('inputs/day1.txt')))
    print('Silver:', totals[-1])
    print('Gold:', sum(totals[-3 : ]))

def parse_total(chunk):
    return sum(parse_list(chunk, int))

if __name__ == '__main__':
    main()
