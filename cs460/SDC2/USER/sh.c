#include "ucode.c"

int main(int argc, char *argv)
{
  // as sh process
    int pid, status;
    int i, j;
    char cmd[8];
    char cmdline[64];
    i=0;
    while(1){
        printf("argc=%d ", argc);
        while(*argv != 0){
            while(*argv != ' ')
                cmdline[i*8+(j++)] = *argv++;
            i++;
        }
        for (i=0; i<8; i++)
            cmd[i] = cmdline[i];
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

