#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(0));
    printf("%x\n", rand());
    return 0;
}
