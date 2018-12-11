#include "ucode.c"

char str[1280];
char cmd1[128];
char cmd2[128];

main(int argc, char* argv[])
{
    char command;
    int i=0;
    while(1)
    {
        if (argc <= 2)
        {
            command = argv[1];
            if (!strcmp(command, "exit") || !strcmp(command, "cd"))
            {
                exec(command);
            }
            singlecmd(command);
        }
        else
        {
            if (argc == 4){
                strcpy(cmd1, argv[1]);
                strcpy(cmd1, argv[2]);
                strcpy(cmd2, argv[4]);
            }
        }
    }
}

void singlecmd(char* command)
{
    int status;
    int pid = fork();

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

