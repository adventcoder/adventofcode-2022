
import framework
from utils import parse_list

def solve(input):
    totals = sorted(parse_totals(input))
    yield totals[-1]
    yield sum(totals[-3 : ])

def parse_totals(input):
    return [sum(parse_list(chunk, int)) for chunk in input.split('\n\n')]

if __name__ == '__main__':
    framework.main()
