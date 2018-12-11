









//This is l2u.c
#include "ucode.c"

int main(int argc, char *argv[])
{
    char c;
    int f1 = 0;
    int f2 = 0;
    STAT fileinfo;

    if(argc == 1)
    {
        f1 = dup(0);
        f2 = dup(1);
    }
    else if (argc == 2)
    {
        f1 = open(argv[1], 0);
        f2 = dup(1);
    }
    else if(argc == 3)
    {
        f1 = open(argv[1], 0);

        stat(argv[2], &fileinfo);

        if(fileinfo.st_size)
        {
            printf("unlinking file\n");
            unlink(argv[2]);
        }
        creat(argv[2]);
        f2 = open(argv[2], 1);
    }

    while(read(f1, &c, 1))
    {
        if (c >= 97 && c <= 122)
        {
            c -= 32;
        }
        write(f2, &c, 1);
        if(c == '\n')
        {
            write(2, '\r', 1);
        }
        else if(c == '\r')
        {
            write(1, '\n', 1);
            write(2, '\r', 1);
        }

    }
    return;
}
//End of l2u.c
