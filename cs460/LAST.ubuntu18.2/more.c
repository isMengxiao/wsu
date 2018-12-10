#include "ucode.c"

#define rows 20

int main(int argc, char* argv[])
{
    char str[64];
    int i=0;
    int fd;

    fd = open(argv[1], O_RDONLY);

    while(i<rows)
    {
        readline(fd, str);
        printf("%s.%d", str, i);
    }
    while(readline(fd, str))
    {
        printf("%s", str);
        getc();
    }

}
