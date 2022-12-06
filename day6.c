
#include <stdio.h>

int start(unsigned char *p, int n, int m) {
  int counts[256] = { 0 };
  int distinct_count = 0;
  #define inc(c) distinct_count += (++counts[c] == 1)
  #define dec(c) distinct_count -= (counts[c]-- == 1)
  for (int i = 0; i < m; i++)
    inc(p[i]);
  for (int i = m; i < n; i++) {
    if (distinct_count == m)
      return i;
    dec(p[i - m]);
    inc(p[i]);
  }
  if (distinct_count == m)
    return n;
  return -1;
}

int main(void) {
  unsigned char packet[1024 * 1024];
  int c;
  int n = 0;
  while ((c = getchar()) != EOF)
    packet[n++] = (unsigned char) c;
  printf("%d\n", start(packet, n, 4));
  printf("%d\n", start(packet, n, 14));
  return 0;
}
