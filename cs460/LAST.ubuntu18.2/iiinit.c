/********************* init.c file ****************/
#include "ucode.c"
int console;
int uart1;
int uart2;

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
        if (pid==uart1){
            printf("INIT: forks a new uart1 login\n");
            uart1 = fork();
            if (uart1)
                continue;
            else
                exec("login /dev/ttyS0");
        }
        if (pid==uart2){
            printf("INIT: forks a new uart2 login\n");
            uart2 = fork();
            if (uart2)
                continue;
            else
                exec("login /dev/ttyS1");
        }
        printf("INIT: I just buried an orphan child proc %d\n", pid);
    }
}
main()
{
    int in, out;
    in= open("/dev/tty0", O_RDONLY); // file descriptor 0
    out = open("/dev/tty0", O_WRONLY); // for display to console
    printf("INIT : fork a login proc on console\n");
    console = fork();
    another_fork();
    if (console) // parent
        parent();
    else
        // child: exec to login on tty0
        exec("login /dev/tty0");
}
int another_fork()
{
    int in1, out1;
    int in2, out2;
    in1  = open("/dev/ttyS0", O_RDONLY);
    in2  = open("/dev/ttyS1", O_RDONLY);
    out1 = open("/dev/ttyS0", O_WRONLY);
    out2 = open("/dev/ttyS1", O_WRONLY);
    printf("INIT : fork login process on 2 UARTS");
    uart1 = fork();
    uart2 = fork();

}
