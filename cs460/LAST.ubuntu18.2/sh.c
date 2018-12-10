#include "ucode.c"

typedef struct{
    char cmd[64];
}CMD;

main(int argc, char* argv[])
{
    char command[64];
    CMD cmds[16];
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
            singlecmd(command)
        }
        else
        {
            while(argv[i++])
            {

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

void do_pipe()
{
    int pid, pd[2];
    pipe(pd);
    pid = fork();
    if (pid)
    {
        close(pd[1]);
        dup2(pd[0], 0);
        exec(cmd2);
    }
    else
    {
        close(pd[0]);
        dup2(pd[1], 1);
        exec(cmd1);
    }
}
