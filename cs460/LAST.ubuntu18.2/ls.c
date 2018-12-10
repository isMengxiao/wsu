char *t1 = "xwrxwrxwr-------";
char *t2 = "----------------";
struct STAT mystat, *sp;
int ls_file(char *fname)
    // list a single file
{
    struct STAT fstat, *sp = &fstat;
    int r, i;
    char sbuf[4096];
    r = lstat(fname, sp);
    /***
    if (S_ISDIR(sp->st_mode))
        printf("%c",'d');
    if (S_ISREG(sp->st_mode))
        printf("%c",'-');
    if (S_ISLNK(sp->st_mode))
        printf("%c",'l');
        ***/
    for (i=8; i>=0; i--){
        if (sp->st_mode & (1<<i))
            printf("%c", t1[i]); // print permission bit as r w x
        else
            printf("%c", t2[i]); // print permission bit as -
    }
    printf("%4d ", sp->st_nlink); // link count
    printf("%4d ", sp->st_uid // uid
            printf("%8d ", sp->st_size); // file size
            strcpy(ftime, ctime(&sp->st_ctime));
            ftime[strlen(ftime)-1] = 0; // kill \n at end
            printf("%s ",ftime); // time in calendar form
            printf("%s", basename(fname)); // file basename
            if (S_ISLNK(sp->st_mode)){ // if symbolic link
            r = readlink(fname, sbuf, 4096);
            printf(" -> %s", sbuf);
            }
            printf("\n");
            }
int ls_dir(char *dname)
{
    char name[256];
    DIR *dp;
    struct dirent *ep;
    dp = opendir(dname); // opendir() syscall
    while (ep = readdir(dp)){ // readdir() syscall
        strcpy(name, ep->d_name);
        if (!strcmp(name, ".") || !strcmp(name, ".."))
            continue;
        strcpy(name, dname);
        strcat(name, "/");
        strcat(name, ep->d_name);
        ls_file(name);
    }
}
int main(int argc, char *argv[])
{
    struct STAT mystat, *sp;
    int r;
    char *s;
    char filename[1024], cwd[1024];
    s = argv[1]; // ls [filename]
    if (argc == 1) // no parameter: ls CWD
        s = "./";
    sp = &mystat;
    if ((r = stat(s, sp)) < 0){ // stat() syscall
        perror("ls"); exit(1);
    }
    strcpy(filename, s);
    if (s[0] != '/'){
        getcwd(cwd, 1024);
        strcpy(filename, cwd);
        strcat(filename, "/");
        strcat(filename,s);
    }
    if (S_ISDIR(sp->st_mode))
        ls_dir(filename);
    else
        ls_file(filename);
}
