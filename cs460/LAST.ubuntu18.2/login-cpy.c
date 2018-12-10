/**************************login.c***********************/
#include "ucode.c"
int in, out, err;
char names[128], password[128];
//char data[1280];
typedef struct
{
    char name[128];
    char pwd[128];
    int gid;
    int uid;
    char fullname[128];
    char HOMEDIR[128];
    char program[128];
} User;

char* splitline(char *string)
{
    char* str = string;
    while(*str != ':' && *str != '\0' && *str != '\n')
    {
        str++;
    }
    *str = '\0';
    return ++str;
}

int sToi(char* str)
{
    int n = 0;
    while(*str != '\0')
    {
        n *= 10;
        n += (int)((char)*str - '0');
        str++;
    }
    return n;
}
int splitUsers(User *user, int file)
{
    char data[128];
    char *newdata;
    char *olddata;
    if (!readline(file, data))
    {
        //printf("Error, no users");
        return 0;
    }
    //printf("data:%s", data);

    newdata = splitline(data);
    strcpy(user->name, data);

    olddata = newdata;
    newdata = splitline(newdata);

    strcpy(user->pwd, olddata);

    olddata = newdata;
    newdata = splitline(newdata);
    olddata = (int)((char)*olddata-'0');
    user->gid = olddata;

    olddata = newdata;
    newdata = splitline(newdata);
    olddata = (int)((char)*olddata-'0');
    user->uid = olddata;

    olddata = newdata;
    newdata = splitline(newdata);
    strcpy(user->fullname, olddata);

    olddata = newdata;
    newdata = splitline(newdata);
    strcpy(user->HOMEDIR, olddata);

    olddata = newdata;
    newdata = splitline(newdata);
    strcpy(user->program, olddata);
}

int getuserlist(User *users)
{
    int filedata;
    filedata = open("/etc/passwd", O_RDONLY);

    User *ThisUser = users;
    while(splitUsers(ThisUser, filedata))
    {
        ThisUser++;
    }

    //close(filedata);
    //printf("\nfile closed.\n");
}

User* getUser(User* users, char* name)
{
    User* ThisUser = users;

    while(ThisUser)
    {

        if (!strcmp(name, ThisUser->name))
            return ThisUser;
        ThisUser++;
    }

    return 0;
}

int PrintUser(User* user)
{
    printf("username: %s. ", user->name);
    printf("password: %s. ", user->pwd);
    printf("gid: %d. ", user->gid);
    printf("uid: %d. ", user->uid);
    printf("fullname: %s. ", user->fullname);
    printf("homedir: %s. ", user->HOMEDIR);
    printf("program: %s. ", user->program);
}

main(int argc, char *argv[])
{
    /**
    char passwd[128];
    char line[256];
    int uid, gid;
    char uname[128];
    char pswd[128];
    char fullname[128], HOMEDIR[128], program[128];
    **/
    int fd;
//1.close file descriptors 0,1 inherited from INIT
    close(0); close(1);
//2.open argv[1] times as in(0), out(1), err(2)
    in  = open("/dev/tty0", O_RDONLY);
    out = open("/dev/tty0", O_WRONLY);
    err = open("/dev/tty0", O_WRONLY);
    // in = open(argv[1], O_RDONLY);

    settty(argv[1]);//3.
    //fd = open("/etc/passwd", O_RDONLY);//4.

    User userlist[100];

    getuserlist(userlist);

    User* ThisUser=0;

    while(1){
        printf("login:");  gets(names);
        ThisUser = getUser(userlist, names);
        printf("Get OK");

        if(!ThisUser)
        {
            printf("Don't have this user");
            continue;
        }

        printf("password:");    gets(password);
        if (strcmp(password, ThisUser->pwd))
        {
            printf("Wrong password!");
            continue;
        }
/**
        strcpy(uname, splitline(line));
        strcpy(pswd,  splitline(line));
        gid = sToi(splitline(line));
        uid = sToi(splitline(line));
        strcpy(fullname, splitline(line));
        strcpy(HOMEDIR,  splitline(line));
        strcpy(program, splitline(line));
**/
        printf("user %s login!!!!!!", ThisUser->name);
        //for each line in /etc/passwd file do
        //tokenize user account line;
        chuid(ThisUser->uid, ThisUser->gid);
        chdir(ThisUser->HOMEDIR);
        //exec("sh");
        close("/etc/passwd");
        exec(ThisUser->program);
    }
    printf("login failed, try again\n");
}

