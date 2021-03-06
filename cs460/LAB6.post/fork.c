int body();
int goUmode();
char *istring = "init start";

PROC *kfork(char *filename)
{
  // called by P0 to creat P1 with /bin/init as Umode image
    int i;
    char *cp, *cq;
    char *addr;
    char line[8];
    int usize1, usize;
    int *ustacktop, *usp;
    u32 BA, Btop, Busp;

    PROC *p = dequeue(&freeList);
    if (p ==0 ){
        kprintf("kfork failed\n");
        return (PROC *)0;
    }
    p->ppid   = running->pid;
    p->parent = running;
    p->status = READY;
    p->priority = 1;

    for (i=1; i<29; i++)
        p->kstack[SSIZE-i] = 0;
    p->kstack[SSIZE-15] = (int)goUmode;
    p->ksp = &(p->kstack[SSIZE-28]);

    load(filename, p);

    BA = p->pgdir[2048] & 0xFFF00000;
    Btop = BA + 0x100000;
    Busp = Btop - 32;

    cp = (char *)Busp;
    strcpy(cp, istring);

    p->kstack[SSIZE-14] = (int)(0x80100000 - 32);

    p->usp = (int *)(0x80100000 - 32);
    p->upc = (int *)0x80000000;
    p->ucpsr = (int *)0x10;

    p->kstack[SSIZE-1] = VA(0);

    enqueue(&readyQueue, p);
    kprintf("proc %d kforked a child %d: ", running->pid, p->pid);
    printQ(readyQueue);

    return p;
}

int fork()
{
  // fork a CHILD process as in Unix/Linux
    int i;
    char *PA, *CA;
    PROC *p = get_proc(&freeList);
    if (p == 0){
        kprintf("fork failed\n");
        return -1;
    }
    p->ppid   = running->pid;
    p->parent = running;
    p->status = READY;
    p->priority = 1;

    PA = (char *)(running->pgdir[2048] & 0xFFFF0000);
    CA = (char *)(p->pgdir[2048] & 0xFFFF0000);
    memcpy(CA, PA, 0x100000);
    for (i=1; i<=14; i++){
        p->kstack[SSIZE-i] = running->kstack[SSIZE-i];
    }
    for (i=15; i<=28; i++)
        p->kstack[SSIZE-i] = 0;


    p->kstack[SSIZE-14] = 0;
    p->kstack[SSIZE-15] = (int)goUmode;
    p->ksp = &(p->kstack[SSIZE-28]);
    p->usp = running->usp;
    p->ucpsr = running->ucpsr;
    enqueue(&readyQueue, p);
    return p->pid;
}
