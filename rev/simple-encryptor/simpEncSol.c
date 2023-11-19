#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(void) {
    typedef unsigned char byte;
    FILE *encFile;
    size_t flagSize;
    byte *flag;
    unsigned int seed;
    int random1, random2;
    long i;

    // this code block is followed similar to what we got after decompiluing the main
    encFile = fopen("flag.enc", "rb");
    // get file size using fseek till end of file
    fseek(encFile, 0, SEEK_END);
    flagSize = ftell(encFile);
    // seek to the starting
    fseek(encFile, 0, SEEK_SET);
    flag = malloc(flagSize+1);
    // this reads data from encFile of size flagSize and stores it in the flag buffer
    fread(flag, 1, flagSize, encFile);
    fclose(encFile);

    // getting the seed value from the buffer
    int offset = 4;
    memcpy(&seed, flag, offset);
    srand(seed);

    // loop for reversing the enc algorithm
    for(i = offset; i < (long)flagSize; i++) {
        random1 = rand();
        random2 = rand();
        // This masking is being done so that random2 is not greater than 8 as if goes beyond it then it will create some weird result
        // this we realized later after getting those weird results
        random2 = random2 & 7;

        flag[i] = flag[i] >> random2 | flag[i] << 8 - random2;
        flag[i] = random1 ^ flag[i];
        printf("%c", flag[i]);
    }
}