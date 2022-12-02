
from utils import *

def main():
    total1 = 0
    total2 = 0
    for a, b in read_table('inputs/day2.txt'):
        i = 'ABC'.index(a)
        j = 'XYZ'.index(b)
        total1 += score(i, j, (j - i + 1) % 3)
        total2 += score(i, (j + i - 1) % 3, j)
    print('Silver:', total1)
    print('Gold:', total2)

def score(shape1, shape2, outcome):
    return shape2 + 1 + outcome * 3

if __name__ == '__main__':
    main()
