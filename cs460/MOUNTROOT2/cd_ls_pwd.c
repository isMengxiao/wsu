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
           // while ((char *)dp < &buf2[BLKSIZE])
            //{
                printf("filename:%s,", dp->name);
            //}
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

    int ino, i;
    MINODE *mip;
    char buf[BLKSIZE];
    char *cp;
    int j;
    INODE *ip;
    ino = getino(dname);
    printf("ino:%d,",ino);
    mip = iget(dev, ino);
    ip = &mip->INODE;

    printf("iblock:%d,%d", ip->i_block[0],ip->i_uid);
    get_block(dev, ip->i_block[0], buf);
    dp = (DIR *)buf;
    cp = buf;
    while (dp < buf + BLKSIZE)
    {
        printf("\n%d,name:",dp->name_len);
        for (j=0; j < dp->name_len; j++){
            printf("%c,",dp->name[j]);
            printf("%d,",dp->inode);
            //    name[j] = dp->name[j];
        }
        //printf("i_number: %d,dirname:%s,", dp->inode, name);
        cp += dp->rec_len;
        printf(",rec_len:%d",dp->rec_len);
        dp = (DIR *)cp;
    }
    printf("\n");

    ls_file(ino);
}

int pwd(MINODE *wd)
{
    if (wd == root)
        printf("/");
    else
        rpwd(wd);
}

int rpwd(MINODE *wd)
{
    INODE *ip;
    if (wd == root)
        return;
    //from i_block[0] of wd->INODE
    //Have not finished ....!!!!!!!!!!
    ip = &wd->INODE;
}
