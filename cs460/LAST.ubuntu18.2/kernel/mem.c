/***************** mem.c file: Dynamic Paging ***************/
int *pfreeList, *last;
int mkPtable()
// called from ts.s, create initial ptable at 16KB
{
int i;
int *ut = (int *)0x4000; // at 16KB
u32 entry = 0 | 0x41E; // AP=01(Kmode R|W; Umode NO) domaian=0
for (i=0; i<4096; i++) // clear 4096 entries to 0
ut[i] = 0;
for (i=0; i<258; i++){
// fill in low 258 entries ID map to PA
ut[i] = entry;
entry += 0x100000;
}
}
int *palloc()
// allocate a page frame
{
int *p = pfreeList;
if (p)
pfreeList = (int *)*p;
return p;
}
void pdealloc(int *p)
287
// deallocate a page frame
{
*last = (int)(*p);
*p = 0;
last = p;
}
// build pfreeList of free page frames
int *free_page_list(int *startva, int *endva)
{
int *p;
printf("build pfreeList: start=%x end=%x : ", startva, endva);
pfreeList = startva;
p = startva;
while(p < (int *)(endva-1024)){
*p = (int)(p + 1024);
p += 1024;
}
last = p;
*p = 0;
return startva;
}
int build_ptable()
{
int *mtable = (int *)0x8000; // new pgdir at 32KB
int i, j, *pgdir, paddr;
printf("build Kmode pgdir at 32KB\n");
for (i=0; i<4096; i++){
// zero out mtable[ ]
mtable[i] = 0;
}
printf("build Kmode pgtables in 5MB\n");
for (i=0; i<258; i++){
// point to 258 pgtables in 5MB
pgtable = (int *)(0x500000 + i*1024);
mtable[i] = (int)pgtable | 0x11; // 1KB entry in 5MB
paddr = i*0x100000 | 0x55E;
// AP=01010101 CB=11 type=10
for (j=0; j<256; j++){
pgtable[j] = paddr + j*4096; // inc by 4KB
}
}
printf("build 64 proc pgdirs at 6MB\n");
for (i=0; i<64; i++){
pgdir = (int *)(0x600000 + i*0x4000); // 16KB each
for (j=0; j<4096; j++){ // zero out pgdir[ ]
pgdir[j] = 0;
}
for (j=0; j<258; j++){ // copy low 258 entries from mtable[]
pgdir[j] = mtable[j];
}
}
}
