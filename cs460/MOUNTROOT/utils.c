int get_block(int dev, int blk, char *buf)
{
    lseek(dev, (long)blk*BLKSIZE, 0);
    read(dev, buf, BLKSIZE);
}

int put_block(int dev, int blk, char *buf)
{
}

int tokenize(char *pathname)
{
}

MINODE *iget(int dev, int ino)
{
}

int iput(MINODE *mip)
{
}

int search(MINODE *mip, char*name)
{
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
