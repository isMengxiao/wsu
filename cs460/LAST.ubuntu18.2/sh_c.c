#include "ucode.c"

typedef struct{
    char cmd[64];
}CMD;

char str[1280];

main(int argc, char* argv[])
{
    char command[64];
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
            while(argv[i++])
                strcpy(str, argv[i]);
            do_pipe(str);
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

void do_pipe(char* str)
{
    int pid, pd[2];
    CMD cmd[10];
    char *cmd1;
    int i=0;
    pipe(pd);
    pid = fork();
    while(*str)
    {
        if(*str == '|')
            strcpy(cmd[i++].cmd, *str++);
        strcpy(cmd[i].cmd, *str++);
    }
    cmd1 = cmd[0].cmd;
    if (pid)
    {
        close(pd[1]);
        dup2(pd[0], 0);
        do_cmd(cmd)
    }
    else
    {
        close(pd[0]);
        dup2(pd[1], 1);
        exec(cmd[0].cmd);
    }
}

void do_cmd(CMD* cmd)
{
    while(cmd->cmd)
    {
        exec(cmd->cmd);
        do_cmd(cmd++);
    }
}
