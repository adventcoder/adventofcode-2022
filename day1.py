
import sys

def main():
    totals = []
    for chunk in open('inputs/day1.txt').read().rstrip().split('\n\n'):
        totals.append(sum(map(int, chunk.split('\n'))))
    totals.sort()
    print('silver:', totals[-1])
    print('gold:', sum(totals[-3 : ]))

if __name__ == '__main__':
    main()
