

#define BLK 1024
char buf1[BLK], buf2[BLK];

INODE *ip;
GD *gp;
DIR *dp;
SUPER *sup;
int get_block(int blk, char *buf)
{
    char *cp = disk + blk*BLKSIZE;
    memcpy(buf, cp, BLKSIZE);
}
int put_block(int blk, char *buf)
{
    char *cp = disk + blk*BLKSIZE;
    memcpy(cp, buf, BLKSIZE);
}

u16 search(INODE *ip, char *name)
{
  //search for name in the data block of INODE;
  //return its inumber if found
  //else error();
    int c,i;
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
                if(strcmp(dp->name,name))
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
int tryloader(char *filename, PROC *p)
{
  u16    ii,ino,iblk;
  int filesize;
  char   *name[2];
  char *addr;
  u32 *up;
  name[0]="bin";
  name[1]=filename;
  getblk(1, buf2);
  sup = (SUPER *)buf2;
  if((u16)sup->s_magic != 0xEF53)
      return 0;
  kprintf("perfect!!");
  getc();

}

int loader(char *filename, PROC *p)
{
  u16    ii,ino,iblk;
  int filesize;
  char   *name[2];
  char *addr;
  u32 *up;
  name[0]="bin";
  name[1]=filename;
  getblk(1, buf2);
  sup = (SUPER *)buf2;
  if((u16)sup->s_magic != 0xEF53)
      return 0;
  kprintf("perfect!!");
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

//    if((u16)ip->i_block[12])
//        getblk((u16)ip->i_block[12],buf2);

    filesize = ip->i_size;
    addr = (char *)(0x800000 + (p->pid - 1)*0x100000);
    kprintf("that-s ok!!!");
    memcpy(addr, (u16)ip->i_block, filesize);

/**
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
  **/
}

