
from utils import read_table

def main():
    table = read_table('inputs/day2.txt', ('ABC'.index, 'XYZ'.index))
    print('Silver:', sum(score(i, j, (j - i + 1) % 3) for i, j in table))
    print('Gold:', sum(score(i, (j + i - 1) % 3, j) for i, j in table))

def score(shape1, shape2, outcome):
    return shape2 + 1 + outcome * 3

if __name__ == '__main__':
    main()
