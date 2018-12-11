#include "ucode.c"

#define rows 10
#define line 80

int main(int argc, char* argv[])
{
    char str[64];
    int i=0;
    int fd;

    fd = open(argv[1], O_RDONLY);

    while(i<rows)
    {
        readline(fd, str);
        if (!*str)
            break;
        printf("%s.%d", str, i++);
    }
    while(readline(fd, str))
    {
        if (str > 80)
        printf("%s", str);
        getc();
        printf("next");
    }

}
