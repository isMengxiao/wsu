/****************************************************************************
*                   mount_root Program                                      *
*****************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <ext2fs/ext2_fs.h>
#include <string.h>
#include <libgen.h>
#include <sys/stat.h>

#include "type.h"


MINODE minode[NMINODE];
MINODE *root;
PROC   proc[NPROC], *running;

char gpath[256]; // holder of component strings in pathname
char *name[64];  // assume at most 64 components in pathnames
int  n;

int  fd, dev;
int  nblocks, ninodes, bmap, imap, iblk, inode_start;
char line[256], cmd[32], pathname[256];

MINODE *iget();

/******* WRITE YOUR OWN util.c and others ***********
#include "util.c"
#include "cd_ls_pwd.c"
***************************************************/

//#include "cd_ls_pwd.c"

int init()
{
  int i;
  MINODE *mip;
  PROC   *p;

  printf("init()\n");

  for (i=0; i<NMINODE; i++){
      mip = &minode[i];
      mip->refCount = 0;// 2. set all entries to 0, except refCount=1
      //mip->dev = 0;//?3. all mtable[].dev = 0?
  }
  for (i=0; i<NPROC; i++){
       p = &proc[i];
       p->pid = i;
       p->uid = i;
       p->cwd = 0;// 1. set pid = i; uid = i; cwd = 0;
  }
  //4. MINODE *root = 0;
  root = 0;
  //3. all mtable[].dev = 0 (as FREE)
  // But, what is mtable
}

// load root INODE and set root pointer to it
int mount_root()
{
  char buf[BLKSIZE];
  SUPER *sp;
  GD    *gp;
  PROC *p;
  int i;

  printf("mount_root()\n");
  /********** read super block at 1024 ****************/
  get_block(dev, 1, buf);
  sp = (SUPER *)buf;

  /* verify it's an ext2 file system *****************/
  if (sp->s_magic != 0xEF53){
      printf("magic = %x is not an ext2 filesystem\n", sp->s_magic);
      exit(1);
  }
  printf("EXT2 FS OK\n");

  ninodes = sp->s_inodes_count;
  nblocks = sp->s_blocks_count;

  printf("\n!!nblocks:%d", nblocks);
  printf("!!ninodes:%d", ninodes);
  // print nblocks, ninodes

  get_block(dev, 2, buf);
  gp = (GD *)buf;

  bmap = gp->bg_block_bitmap;
  imap = gp->bg_inode_bitmap;
  iblk = inode_start = gp->bg_inode_table;

  printf("\nbmap:%d, imap:%d, inodes_start:%d", bmap, imap, iblk);
  // print bmap, imap, inodes_start

  root = iget(dev, 2);       // get #2 INODE into minoe[ ]
  printf("\nmounted root OK\n");

  for (i=0; i<NPROC; i++){
      p = &proc[i];
      p->cwd = iget(dev, 2);
  }
  running = &proc[0];

}

char *disk = "mydisk";
int main(int argc, char *argv[ ])
{
  int ino;
  char buf[BLKSIZE];
  if (argc > 1)
     disk = argv[1];

  fd = open(disk, O_RDWR);
  if (fd < 0){
     printf("open %s failed\n", disk);
     exit(1);
  }
  dev = fd;

  init();
  mount_root();
  printf("root refCount = %d\n", root->refCount);

  printf("creating P0 as running process\n");
  running = &proc[0];
  running->status = READY;
  running->cwd = iget(dev, 2);
  printf("root refCount = %d\n", root->refCount);

  while(1){
    printf("input command : [ls|cd|pwd|quit] ");
    fgets(line, 128, stdin);
    line[strlen(line)-1] = 0;

    if (line[0]==0)
       continue;
    pathname[0] = 0;

    sscanf(line, "%s %s", cmd, pathname);
    printf("cmd=%s pathname=%s\n", cmd, pathname);
    if (strcmp(cmd, "ls")==0)
       ls_dir(pathname);
/***
    if (strcmp(cmd, "cd")==0)
       chdir(pathname);

    if (strcmp(cmd, "pwd")==0)
       pwd(running->cwd);
***/
    if (strcmp(cmd, "quit")==0)
       quit();
  }
}

int print(MINODE *mip)
{
  int blk;
  char buf[1024];
  int i;
  DIR *dp;
  char *cp;

  INODE *ip = &mip->INODE;
  for (i=0; i < 12; i++){
    if (ip->i_block[i]==0)
      return 0;
    get_block(dev, ip->i_block[i], buf);
    dp = (DIR *)buf; cp = buf;
    while(cp < buf+1024){
      printf("%d %d %d %s\n", dp->inode, dp->rec_len, dp->name_len, dp->name);
      cp += dp->rec_len;
      dp = (DIR *)cp;
    }
  }
}

int quit()
{
  int i;
  MINODE *mip;
  for (i=0; i<NMINODE; i++){
    mip = &minode[i];
    if (mip->refCount > 0)
      iput(mip);
  }
  exit(0);
}
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
        printf("/")
    else
        rpwd(wd);
}

int rpwd(MINODE *wd)
{
    INODE *ip;
    if (wd == root)
        return;
    //from i_block[0] of wd->INODE
    ip = &wd->INODE;
}
