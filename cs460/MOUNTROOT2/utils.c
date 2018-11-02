int get_block(int dev, int blk, char *buf)
{
    lseek(dev, (long)blk*BLKSIZE, 0);
    read(dev, buf, BLKSIZE);
}

int put_block(int dev, int blk, char *buf)
{
    lseek(dev, (long)blk*BLKSIZE, 0);
    write(dev, buf, BLKSIZE);
}

int tokenize(char *pathname)
{
    int i;
    char *cp;
    cp = path;
    nn = 0;

    while (*cp != 0){
        while (*cp == '/') *cp++ = 0;
        if (*cp != 0)
            name[nn++] = cp;
        while (*cp != '/' && *cp != 0) cp++;
        if (*cp != 0)
            *cp = 0;
        else
            break;
        cp++;
    }

    printf("n = %d : ", nn);
    for (i=0; i<nn; i++)
        printf("  %s  ", name[i]);
    printf("\n");
}

MINODE *iget(int dev, int ino)
{
}

int iput(MINODE *mip)
{
}

int search(MINODE *mip, char*name)
{
   int i;
   char c, *cp;
   INODE *ip;
   DIR  *dp;
   ip = &mip->INODE;
   for (i=0; i<12; i++){
       if ( ip->i_block[i] ){
         printf("i_block[%d] = %d\n", i, ip->i_block[i]);

	 getblk(ip->i_block[i], b2);
          cp = b2;
          dp = (DIR *)b2;

          while (cp < b2 + BLKSIZE){
              c = dp->name[dp->name_len];  // save last byte
              dp->name[dp->name_len] = 0;
	      printf("%s ", dp->name);
              if ( strcmp(dp->name, name) == 0 ){
		 printf("FOUND %s\n", name);
                 return(dp->inode);
              }
              dp->name[dp->name_len] = c; // restore that last byte
              cp += dp->rec_len;
              dp = (DIR *)cp;
	}
     }
   }
   return 0;
}


int getino(char *pathname)
{

}

int findmyname(MINODE *parent, u32 myino, char *myname)
{
}

int findino(MINODE *mip, u32 *myino)
{
}
