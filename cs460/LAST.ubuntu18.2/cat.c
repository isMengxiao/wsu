#include "ucode.c"


main(int argc, char* argv[])
{
    int i=0;
    char str[1280];
    int file;
    int file1, file2;
    STAT FileInfo;
    int filesize;
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
        if (argv[2] == '\0')
        {
            file = open(argv[1], O_RDONLY);
            stat(argv[1], &FileInfo);
            filesize = FileInfo.st_size;
            read(file, str, filesize);
            close(file);
            printf("%s", str);
        }
        else if (argv[1] == '>')
        {
            //dup2(1, argv[2]);
            file = open(argv[2], O_WRONLY);
            printc('\n');
            gets(str);
            printf("%s", str);
            write(file, str, strlen(str));
            close(file);
        }
        else
        {
            if (argv [2] == '>')
            {
                dup2(argv[1], argv[3]);
                /**
                strcat(str, "cp ");
                strcat(str, argv[1]);
                strcat(str, argv[3]);
                printf("command:%s", str);
                exec(str);
                **/
            }
            else if (argv [2] == '>>')
            {
                file2 = open(argv[3], 2);
                file1 = open(argv[1], O_RDONLY);
                stat(argv[1], &FileInfo);
                filesize = FileInfo.st_size;
                read(file, str, filesize);
                write(file, str, filesize);
                close(file1);
                close(file2);
            }
            printf("Error command");
        }
    }


}
