/***
int load(char *filename, PROC *p)
{
  // load filename to p's Umode area
}
***/

#define BLK 1024
char buf1[BLK], buf2[BLK];
int getblk(int blk, char *buf);
int putblk(int blk, char *buf);

INODE *ip;
GD *gp;
DIR *dp;
SUPER *sup;

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
                //kprintf("\n");kputc(' ');
                if(!strcmp(dp->name,name))
                {
                    kprintf("Compare%s,%s",dp->name,name);
                    //kprintf("\n\r");
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
  kgetc();

}

int load(char *filename, PROC *p)
{
  u16    ii,ino,iblk;
  int filesize;
  char   *name[2];
  char *addr;
  char file[128];
  int i;
  u32 *up;
  i = 0;
  if (*filename != '/')
      strcpy(name[0], "bin");
  else{
    while(*filename && (*filename!='/' ))
      file[i++] = *filename++;
    strcpy(name[0], file);
  }
  i = 0;
  while(*filename)
      file[i++] = *filename++;
  while(file[i])
      file[i++] = 0;
  strcpy(name[1], file);

  getblk(1, buf2);
  sup = (SUPER *)buf2;
  if((u16)sup->s_magic != 0xEF53)
      return 0;
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
    //kprintf("that-s ok!!\n\n\nI find it!!!!");
    //memcpy(addr, (u16)ip->i_block, 12*BLKSIZE);

//    if INODE has indirect blocks: get i_block[12] int buf2[  ]
    getblk(ip->i_block[12], buf2);
    kprintf("BLock12:%d\n",ip->i_block[12]);



//setes(0x1000);  // MTX loading segment = 0x1000

//3. load 12 DIRECT blocks of INODE into memory
   for (i=0; i<12; i++){
      kprintf("block:%d  ",(u16)ip->i_block[i]);
      getblk((u16)ip->i_block[i], addr+i*BLKSIZE);
   }
//4. load INDIRECT blocks, if any, into memory
   if (ip->i_block[12]){
     up = (u32 *)buf2;
     while(*up){
        getblk((u16)*up, addr+(i++)*BLKSIZE);
        kprintf("indirblock:%d ", up++);
     }
  }
//**  **/
}

