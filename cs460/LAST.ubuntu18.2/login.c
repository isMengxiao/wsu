/**************************login.c***********************/
#include "ucode.c"
int in, out, err;
char name[128], password[128]
main(int argc, char *argv[])
{
    char passwd[128];
    char line[256];
    int uid, gid;
//1.close file descriptors 0,1 inherited from INIT
    close(0); close(1); close(2);
//2.open argv[1] times as in(0), out(1), err(2)
    in  = open(tty, 0);
    out = open(tty, 1);
    err = open(tty, 2);

    settty(argv[1]);//3.

    password = open("etc/passwd", O_RDONLY);//4.
    while(1){
        printf("login:");   gets(name);
        printf("password:");    gets(passwd);
        readline(password, line);
        //for each line in /etc/passwd file do
        //tokenize user account line;
        chuid();
        chdir(home);
        close();
        exec();
    }
    printf("login failed, try again\n");
}
