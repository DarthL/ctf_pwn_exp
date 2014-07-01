#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char *str="\x0F\x8E\x9E\x39\x3D\x5E\x3F\xA8"\
                 "\x7A\x68\x0C\x3D\x8B\xAD\xC5\xD0"\
                 "\x7B\x09\x34\xB6\xA3\xA0\x3E\x67\x5D\xD6";

signed int my_pow(int a1, unsigned int a2){
    unsigned int i;
    signed int v4;

    v4 = 1;
    for (i = 0; i < a2; ++i)
        v4 *= a1;
    return v4;
}

int __ROL__(int a, int b){
    return (a<<b)|((unsigned)a>>(32-b));
}

char* decode(const char* a1, int a2, int a3){
    unsigned int size;
    int j;
    char *v8;
    size = strlen(a1) + 1;
    v8 = (char *)malloc(size);
    memset(v8, 0, size);
    for (j = 0; j < (signed int)(size - 1); j += 2){
        v8[j] = a2 ^ a1[j];
        a2 = __ROL__(a2, 5) ^ 0x2f;
        if (!a1[j+1])
            break;
        v8[j+1] = a3 ^ a1[j+1];
        a3 = (unsigned char)a2 ^ __ROL__(a3, 11);
    }
    return v8;
}

int WinMain(int a1, int a2, int counter){
    unsigned int new_a1;
    int new_a2;
    int ExitCode, result;

    printf("%s\n", decode(str, a1, a2));
    a1 ^= 0xB72AF098;
    a2 = a1*a2^a2;

    new_a1 = 29 * a1 + 7 * my_pow(a1, 2);
    new_a2 = my_pow(new_a1 ^ a2, new_a1 % 2 + 5);
    if((unsigned int)a1 <= 0xD0000000){
        do{
            if( (unsigned int)counter > 400 )
                return 0;
            ++counter;
            ExitCode = WinMain(new_a1, new_a2, counter);
            new_a1 = ExitCode;
            new_a2 = my_pow(ExitCode ^ new_a2, ExitCode % 0x1E);
        }while(ExitCode);
        result = 0;
    }
    else{
        //result = 13 * new_a1 / 0x1B ^ 0x1F2A990D;
        result = 13 * (new_a1 / 0x1B) ^ 0x1F2A990D;
    }
    return result;
}

int main(){
    WinMain(0xA8276BFA, 0x92F837ED,1);
    return 0;
}
