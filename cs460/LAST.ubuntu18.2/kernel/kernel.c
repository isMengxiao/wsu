/********************* kernel.c file *********************/
#include "../type.h"
PROC proc[NPROC+NTHREAD];
PRES pres[NPROC];
PROC *freelist, *tfreeList, *readyQueue, *sleepList, *running;;
int sw_flag;
int procsize = sizeof(PROC);
OFT oft[NOFT];
PIPE pipe[NPIPE];
int kernel_init()
{
    int i, j;
    PROC *p; char *cp;
    printf("kernel_init()\n");
    for (i=0; i<NPROC; i++){ // initialize PROCs in freeList
        p = &proc[i];
        p->pid = i;
        p->status = FREE;
        p->priority = 0;
        p->ppid = 0;
        p->res = &pres[i];
        // res point to pres[i]
        p->next = p + 1;
        // proc[i]'s umode pgdir and pagetable are at 6MB + pid*16KB
        p->res->pgdir = (int *)(0x600000 + (p->pid-1)*0x4000);
    }
    proc[NPROC-1].next = 0;
    freeList = &proc[0];
    // similar code to initialize tfreeList for NTHREAD procs
    readyQueue = 0;
    sleepList = 0;
    // create P0 as the initial running process;
    p = running = get_proc(&freeList);
    p->status = READY;
    p->res->uid = p->res->gid = 0;
    p->res->signal = 0;
    p->res->name[0] = 0;
    p->time = 10000;
    // arbitrary since P0 has no time limit
    p->res->pgdir = (int *)0x8000; // P0's pgdir at 32KB
    for (i=0; i<NFD; i++)
        // clear file descriptor array
        p->res->fd[i] = 0;
    for (i=0; i<NSIG; i++) // clear signals
        p->res->sig[i] = 0;
    build_ptable();
    // in mem.c file
    printf("switch pgdir to use 2-level paging : ");
    switchPgdir(0x8000);
    // build pfreelist: free page frames begin from 8MB end = 256MB
    pfreeList = free_page_list((int *)0x00800000, (int *)0x10000000);
    pipe_init(); // initialize pipes in kernel
    mbuf_init(); // initialize message buffers in kernel
}
