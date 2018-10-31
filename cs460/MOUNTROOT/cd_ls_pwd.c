int ls_file(int ino)
{
    MINODE *mip;
    char buf[BLKSIZE];
    char buf2[BLKSIZE];
    DIR *dp;
    int i;

    mip = iget(dev, ino);
    for (i=1; i<12; i++)
        if((u16)mip->INODE.i_block[i])
        {
            get_block((u16)mip->INODE.i_block[i], 1, buf2);
            dp = (DIR *)buf2;
            while ((char *)dp < &buf2[BLKSIZE])
            {
                printf("filename:%s,", dp->name);
            }
        }

    /***
    struct stat fstat, *sp = &fstat;
    int r, i;
    char sbuf[4096];
    r = lstat(fname, sp);
    if (S_ISDIR(sp->st_mode))
        printf("%c", 'd');
    if (S_ISREG(sp->st_mode))
        printf("%c", '-');
    if (S_ISLNK(sp->st_mode))
        printf("%c", 'l');
    for (i=8; i>=0; i--){
        if (sp->st_mode & (1<<i))
            printf("%c", t1[i]);
        else
            printf("%c", t2[i]);
    }
    printf("%4d", sp->st_nlink);
    printf("%4d", sp->st_uid);
    printf("%8d", sp->st_size);
    strcpy(ftime, ctime(&sp->st_ctime));

    ftime[strlen(ftime)-1] = 0;
    printf("%s ", ftime);
    printf("%s", basename(fname));
    if (S_ISLNK(sp->st_mode)){
        r = readlink(fname, sbuf, 4096);
        printf(" -> %s", sbuf);
    }
    printf("\n")
    ***/
}

int ls_dir(char *dname)
{
    char name[256];
    DIR *dp;
    struct dirent *ep;

    int ino;
    MINODE *mip;
    char buf[BLKSIZE];

    ino = getino(dname);
    mip = iget(dev, ino);

    get_block(mip->INODE.i_block[0], 1, buf);
    dp = (DIR *)buf;
    while ((char *)dp < &buf[BLKSIZE])
    {
        printf("name:%s,", dp->name);
    }
    printf("\n");

    ls_file(ino);
}

