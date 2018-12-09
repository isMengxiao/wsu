//Image file booter's bc.c code
#include "ext2.h"
#define BLK 1024
typedef unsigned char  u8;
typedef unsigned short u16;
typedef unsigned long  u32;
typedef struct ext2_group_desc  GD;
typedef struct ext2_inode       INODE;
typedef struct ext2_dir_entry_2 DIR;
u16 NSEC = 2;
cahr buf1[BLK], buf2[BLK];
int prints(char *s)
