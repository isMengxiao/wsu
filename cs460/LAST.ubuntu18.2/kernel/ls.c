/** Program C8.2: ls.c: run as a.out [filename] **/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
char *t1 = "xwrxwrxwr-------";
char *t2 = "----------------";
struct stat mystat, *sp;
int ls_file(char *fname)
// list a single file
{
struct stat fstat, *sp = &fstat;
int r, i;
char sbuf[4096];
r = lstat(fname, sp);
// lstat the file
if (S_ISDIR(sp->st_mode))
printf("%c",'d');
// print file type as d
if (S_ISREG(sp->st_mode))
printf("%c",'-');
// print file type as -
if (S_ISLNK(sp->st_mode))
printf("%c",'l');
// print file type as l
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
// -> linked pathname
}
printf("\n");
}
int ls_dir(char *dname)
// list a DIR
{
char name[256];
// EXT2 filename: 1-255 chars
DIR *dp;
struct dirent *ep;
// open DIR to read names
dp = opendir(dname); // opendir() syscall
while (ep = readdir(dp)){ // readdir() syscall
strcpy(name, ep->d_name);
if (!strcmp(name, ".") || !strcmp(name, ".."))
continue;
// skip over . and .. entries
strcpy(name, dname);
strcat(name, "/");
strcat(name, ep->d_name);
ls_file(name);
// call list_file()
}
}
int main(int argc, char *argv[])
{
struct stat mystat, *sp;
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
// filename is relative to CWD
// get CWD path
strcpy(filename, cwd);
strcat(filename, "/");
strcat(filename,s);
// construct $CWD/filename
}
if (S_ISDIR(sp->st_mode))
ls_dir(filename);
// list DIR
else
ls_file(filename);
// list single file
}
