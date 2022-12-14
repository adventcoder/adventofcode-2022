
import framework
from utils import parse_table

def solve(input):
    table = parse_table(input, ('ABC'.index, 'XYZ'.index))
    yield sum(score(i, j, (j - i + 1) % 3) for i, j in table)
    yield sum(score(i, (j + i - 1) % 3, j) for i, j in table)

def score(your_shape, my_shape, outcome):
    return my_shape + 1 + outcome * 3

if __name__ == '__main__':
    framework.main()
