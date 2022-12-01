
import sys

def main():
    totals = read_totals('inputs/day1.txt')
    totals.sort()
    print('silver:', totals[-1])
    print('gold:', sum(totals[-3 : ]))

def read_totals(path):
    return [sum(map(int, chunk.split('\n'))) for chunk in read(path).rstrip().split('\n\n')]

def read(path):
    with open(path) as file:
        return file.read()

if __name__ == '__main__':
    main()
