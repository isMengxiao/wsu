








//This is sh.c
#include "ucode.c"

char str[1280];
char cmd1[128];
char cmd2[128];

main()
{
    char cmd[128];
    int i=0;
    while(1)
    {
        printf("start sh");
        printf("Command:");
        gets(cmd1);
        if (1)
        {
            printf("single cmd");
            printf("result:%d", strcmp(cmd1, "exit"));
            if (!strcmp(cmd1, "exit"))
            {
                printf("easy cmd");
                exec(0);
                return 0;
            }
            printf("run");
            singlecmd(cmd1);
        }
        else
        {
            printf("complex cmd");
            /**
            if (argc == 4){
                strcpy(cmd1, argv[1]);
                strcpy(cmd1, argv[2]);
                strcpy(cmd2, argv[4]);
                do_pipe(cmd1, cmd2);
            }
            **/
        }
    }
}

void singlecmd(char* command)
{
    int status;
    int pid = fork();

    printf("do run");
    if (pid == 0)
        exec(command);
    else
        pid = wait(&status);
}

void do_pipe(char* cmd1, char* cmd2)
{
    int pid, pd[2];
    pipe(pd);
    pid = fork();
    if(pid){
        close(pd[1]);
        dup2(pd[0], 0);
        exec(cmd2);
    }
    else{
        close(pd[0]);
        dup2(pd[1], 1);
        exec(cmd1);
    }
}

//End of sh.c
