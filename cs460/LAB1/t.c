/*******************************************************
*                  @t.c file                          *
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
    while((*s = getc())!=0x0D)
    {
        putc(*(s++));
    }
    *s = '\0';
}

int str_compare(char *s1, char *s2)
{
    while(*s1&&*s2)
        if(*(s1++)!=*(s2++))
            return 0;
    return 1;
}

u16 NSEC = 2,i;
char *c,buf1[BLK], buf2[BLK];

u16 getblk(u16 blk, char *buf)
{
    readfd( (2*blk)/CYL, ( (2*blk)%CYL)/TRK, ((2*blk)%CYL)%TRK, buf);

    // readfd( blk/18, ((blk)%18)/9, ( ((blk)%18)%9)<<1, buf);
}

u16 search(INODE *ip, char *name)
{
  //search for name in the data block of INODE;
  //return its inumber if found
  //else error();
    for (i=0;i<12;i++)
        if((u16)ip->i_block[i])
        {
            getblk((u16)ip->i_block[i],buf2);
            dp = (DIR *)buf2;
            while ((char *)dp<&buf2[BLK])
            {
                c = dp->name[dp->name_len];
                dp->name[dp->name_len]= 0;
                prints(dp->name);putc(' ');
                if(str_compare(dp->name,name))
                {
                    prints("\n\r");
                    return ((u16)dp->inode)-1;
                }
                dp->name[dp->name_len] = c;
                dp = (char *)dp + dp->rec_len;
            }
        }
   return 0;
}

//u16 str_compare(char *s1,char *s2)
//{
//    while(*s1&&*s2)
 //   {
  //      if(*(s1++)!=*(s2++))
 //           return 0;
//    }
 //   return 1;
//}


main()
{

//1. Write YOUR C code to get the INODE of /boot/mtx
//   INODE *ip --> INODE
  u16    ii,ino,iblk;
  char   *name[2];
  u32 *up;
  name[0]="boot";
  name[1]="mtx";
  getblk(2, buf1);

// 1. WRITE YOUR CODE to get iblk = bg_inode_table block number
  gp = (GD *)buf1;
  iblk = (u16)gp->bg_inode_table;

// 2. WRITE YOUR CODE to get root inode
  getblk(iblk,buf1);
  ip = (INODE *)buf1 + 1;

// 3. WRITE YOUR CODE to step through the data block of root inode
    for (ii=0;ii<2;ii++)
    {
        ino = search(ip,name[ii]);
        getblk(iblk+(ino/8),buf1);
        ip = (INODE *)buf1+(ino%8);
    }

    if((u16)ip->i_block[12])
        getblk((u16)ip->i_block[12],buf2);


//  if INODE has indirect blocks: get i_block[12] int buf2[  ]


setes(0x1000);  // MTX loading segment = 0x1000

//3. load 12 DIRECT blocks of INODE into memory
   for (i=0; i<12; i++){
      getblk((u16)ip->i_block[i], 0);
      putc('*');
      inces();
   }

//4. load INDIRECT blocks, if any, into memory
   if (ip->i_block[12]){
     up = (u32 *)buf2;
     while(*up){
        getblk((u16)*up, 0); putc('.');
        inces();
        up++;
     }
  }
  prints("go?"); getc();
}
