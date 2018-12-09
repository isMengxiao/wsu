/********************* init.c file ****************/
#include "ucode.c"
int console;
int parent()// P1's code
{
    int pid, status;
    while(1){
        printf("INIT : wait for ZOMBIE child\n");
        pid = wait(&status);
        if (pid==console){
            // if console login process died
            printf("INIT: forks a new console login\n");
            console = fork(); // fork another one
            if (console)
                continue;
            else
                exec("login /dev/tty0"); // new console login process
        }
        printf("INIT: I just buried an orphan child proc %d\n", pid);
    }
}
main()
{
    int in, out;
    in  = open("/dev/tty0", O_RDONLY); // file descriptor 0
    out = open("/dev/tty0", O_WRONLY); // for display to console
    printf("INIT : fork a login proc on console\n");
    console = fork();
    if (console) // parent
        parent();
    else
        // child: exec to login on tty0
        exec("login /dev/tty0");
}
