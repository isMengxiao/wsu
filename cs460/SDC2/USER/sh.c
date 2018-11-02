#include "ucode.c"

int main(int argc, char *argv)
{
  // as sh process
    int pid, status;
    int i, j;
    char cmd[8];
    char cmdline[64];
    while(1){
        ugetline(cmdline);
        token(cmdline);
        printf("cmdline!!!:", cmdline);
        strcpy(cmd, cmdline);
        if (!strcmp(cmd, "exit"))
            uexit(0);
        pid = fork();
        if (pid)
            pid = wait(&status);
        else{
            printf("!!!!sh cmdline: %s", cmdline);
            exec(cmdline);
        }
    }
}

