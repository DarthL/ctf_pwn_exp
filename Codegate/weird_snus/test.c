#include <stdio.h>
#include <string.h>

int main()
{
    int i;
    char path[100];
    char* s1 = "Hello";
    char* s2 = "\x00\\123";
    i = memcmp(s1, s2, strlen(s2));
    getcwd(path, 101);
    printf("%d\n", i);
    printf("%s\n", path);
    return 0;
}
