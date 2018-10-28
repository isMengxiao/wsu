#include "ucode.c"

int main(int argc, char *argv[])
{
  // as INIT
    int sh, pid, status;
    sh = fork();
    if (sh){
        while(1){
            pid = wait(&status);
            if (pid == sh){
                sh = fork();
                continue;
            }
            kprintf("P1: I just buried an orphan %d\n", pid);
        }
    }
    else
        exec("sh");
}

