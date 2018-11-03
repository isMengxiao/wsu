#include "ucode.c"

int main(int argc, char *argv)
{
  // as sh process
    int pid, status;
    int i, j;
    char cmd[8];
    char cmdline[64];
    while(1){
        printf("input a command : [u1|u2|exit]: ");
        ugetline(cmdline);
        token(cmdline);
        strcpy(cmd, cmdline);
        //printf("cmdline!!!:%s\n", cmd);
        if (!strcmp(cmd, "exit"))
            uexit(0);
        pid = fork();
        if (pid)
            pid = wait(&status);
        else{
        //    printf("!!!!sh cmdline: %s\n", cmdline);
            exec(cmdline);
        }
    }
}

