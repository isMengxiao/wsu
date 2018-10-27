/*******************************************************
*                      t.c file                        *
*******************************************************/
typedef unsigned char  u8;
typedef unsigned short u16;
typedef unsigned long  u32;

#define TRK 18
#define CYL 36
#define BLK 1024

#include "ext2.h"
typedef struct ext2_group_desc  GD;
typedef struct ext2_inode       INODE;
typedef struct ext2_dir_entry_2 DIR;
GD    *gp;
INODE *ip;
DIR   *dp;

char buf1[BLK], buf2[BLK];
int color = 0x0A;
u8 ino;

main()
{
  u16    i, iblk;
  char   *c, temp[64];
  u16    boot_number;

  prints("read block# 2 (GD)\n\r");
  getblk(2, buf1);

// 1. WRITE YOUR CODE to get iblk = bg_inode_table block number
  gp = (GD *)buf1;
  iblk = (u16)gp->bg_inode_table;
  prints("inode_block="); putc(iblk+'0'); prints("\n\r");

// 2. WRITE YOUR CODE to get root inode
  prints("read inodes begin block to get root inode\n\r");
  getblk(iblk,buf2);
  ip = (INODE *)buf2 + 1;

// 3. WRITE YOUR CODE to step through the data block of root inode
    prints("read data block of root DIR\n\r");
    getblk((u16)ip->i_block[0],buf2);
    dp = (DIR *)buf2;
    c = buf2;
    while(c < buf2+1024)
    {
        for (i=0;i<dp->name_len;i++)
            putc(dp->name[i]);
        if(str_compare(dp->name,"boot"))
        {
            prints("!!!!This is the boot!!");
            boot_number = (u16)dp->inode-1;
        }
        prints("\n\r");
        getc();
        c += dp->rec_len;
        dp = (DIR *)c;
    }

// 4. print file names in the root directory /
    getblk(boot_number/8+iblk,buf2);
    ip = (INODE *)buf2 +(boot_number%8);
    getblk((u16)ip->i_block[0],buf2);
    dp = (DIR *)buf2;
    c = buf2;
    while(c < buf2+1024)
    {
        for (i=0;i<dp->name_len;i++)
            putc(dp->name[i]);
        prints("\n\r");
        getc();
        c += dp->rec_len;
        dp = (DIR *)c;
    }
}

int prints(char *s)
{
    while(*s)
    {
        putc(*(s++));
    }
    return 0;
}

int gets(char *s)
{
    while((*s = getc())!= 0x0D)
    {
        putc(*(s++));
    }
    *s = '\0';
}

int str_compare(char *s1,char *s2)
{
    while(*s1&&*s2)
    {
        if(*(s1++)!=*(s2++))
            return 0;
    }
    return 1;
}

int getblk(u16 blk, char *buf)
{
  // readfd( (2*blk)/CYL, ( (2*blk)%CYL)/TRK, ((2*blk)%CYL)%TRK, buf);
  readfd( blk/18, ((blk)%18)/9, ( ((blk)%18)%9)<<1, buf);
}
