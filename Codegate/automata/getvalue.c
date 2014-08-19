#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    int i;
    int product = 0;
    int value1, value2, value0;
    char command[] = "cat<key>&4";
    for(i = strlen(command); i > 0; --i)
        product = 37 * (product + command[i-1]);

    value1 = product % 0x11 + 1;
    value2 = (product & 0xf) + 1;
    value0 = 43 - value1 - value2;

    printf("value0: %d\n", value0);
    printf("value1: %d\n", value1);
    printf("value2: %d\n", value2);
    return 0;
}
