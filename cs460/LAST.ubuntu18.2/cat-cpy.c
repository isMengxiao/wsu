#include "ucode.c"


main(int argc, char* argv[])
{
    int i=0;
    char str[128];
    int file;
    STAT FileInfo;
    int filesize;
    printf("\nargc:%d", argc);
    if (argc == 1)
    {
        while(1)
        {
            printc('\n');
            gets(str);
            printf("%s", str);
        }
    }
    else
    {
        while(argv[i])
            printf("%s ", argv[i++]);
        if (!argv[2])
        {
            file = open(argv[1], O_RDONLY);
            stat(argv[1], &FileInfo);
            filesize = FileInfo.st_size;
            read(file, str, filesize);
            printf("%s", str);
        }
        else if (argv[1] == '>')
        {
            file = open(argv[2], O_WRONLY);
            printf("It-s > !!!");
            printc('\n');
            gets(str);
            printf("%s", str);
            write(file, str, strlen(str));
        }
        else if (argv[1] == '>>')
        {
            file = open(argv[2], O_WRONLY);
            printf("It-s > !!!");
            printc('\n');
            gets(str);
            printf("%s", str);

        }
    }


}
