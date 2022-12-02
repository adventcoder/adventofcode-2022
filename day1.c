
#include <stdlib.h>
#include <stdio.h>

#define LINE_SIZE 100
#define NUM_TOTALS 3

static int next_total(FILE *input, int *total) {
    int count = 0;
    *total = 0;
    for (;;) {
        static char line[LINE_SIZE];
        if (!fgets(line, LINE_SIZE, input))
            break;
        int num;
        if (sscanf(line, "%d", &num) != 1)
            break;
        *total += num;
        count += 1;
    }
    return count;
}

static void insert(int *totals, int new_total) {
    int i = 0;
    while (i < NUM_TOTALS && new_total > totals[i]) {
        if (i > 0)
            totals[i - 1] = totals[i];
        i++;
    }
    if (i > 0)
        totals[i - 1] = new_total;
}

int main(void) {
    FILE *input = fopen("inputs/day1.txt", "r");
    if (!input) {
        fprintf(stderr, "Input not found!\n");
        return EXIT_FAILURE;
    }

    int top_totals[NUM_TOTALS] = { 0 };
    int total;
    while (next_total(input, &total))
        insert(top_totals, total);

    printf("Silver: %d\n", top_totals[NUM_TOTALS - 1]);

    int tippy_top_total = 0;
    for (int i = 0; i < NUM_TOTALS; i++)
        tippy_top_total += top_totals[i];

    printf("Gold: %d\n", tippy_top_total);

    return EXIT_SUCCESS;
}

