
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#define LINE_SIZE 100

static bool next_total(FILE *input, int *total) {
    int count = 0;
    *total = 0;
    while (true) {
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

static void insert(int *totals, int size, int new_total) {
    if (new_total > totals[0]) {
        totals[0] = new_total;
        for (int i = 1; i < size; i++) {
            if (new_total > totals[i]) {
                totals[i - 1] = totals[i];
                totals[i] = new_total;
            }
        }
    }
}

int main(void) {
    FILE *input = fopen("inputs/day1.txt", "r");
    if (!input) {
        fprintf(stderr, "input not found\n");
        return EXIT_FAILURE;
    }

    int top_totals[] = { 0, 0, 0 };
    int total;
    while (next_total(input, &total))
        insert(top_totals, 3, total);

    int tippy_top_total = 0;
    for (int i = 0; i < 3; i++)
        tippy_top_total += top_totals[i];

    printf("silver: %d\n", top_totals[2]);
    printf("gold: %d\n", tippy_top_total);

    return EXIT_SUCCESS;
}

