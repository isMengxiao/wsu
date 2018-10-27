/********************************************************************
Copyright 2010-2017 K.C. Wang, <kwang@eecs.wsu.edu>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
********************************************************************/

/********************
#define  SSIZE 1024
#define  NPROC  9
#define  FREE   0
#define  READY  1
#define  SLEEP  2
#define  BLOCK  3
#define  ZOMBIE 4
#define  printf  kprintf

typedef struct proc{
  struct proc *next;
  int    *ksp;
  int    status;
  int    pid;

  int    priority;
  int    ppid;
  struct proc *parent;
  int    event;
  int    exitCode;
  int    kstack[SSIZE];
}PROC;
***************************/
#define NPROC 9
PROC proc[NPROC], *running, *freeList, *readyQueue;
int procsize = sizeof(PROC);
int body();

int init()
{
  int i, j;
  PROC *p;
  kprintf("kernel_init()\n");
  for (i=0; i<NPROC; i++){
    p = &proc[i];
    p->pid = i;
    p->status = READY;
    p->next = p + 1;
  }
  proc[NPROC-1].next = 0; // circular proc list
  freeList = &proc[0];
  readyQueue = 0;

  printf("create P0 as initial running process\n");
  p = dequeue(&freeList);
  p->priority = 0;
  p->ppid = 0; p->parent = p;  // P0's parent is itself
  running = p;
  kprintf("running = %d\n", running->pid);
  printList("freeList", freeList);
}

PROC *kfork(int func, int priority)
{
  int i;
  PROC *p = dequeue(&freeList);
  PROC *q = running->child;
  if (p==0){
    printf("no more PROC, kfork failed\n");
    return 0;
  }
  p->status = READY;
  p->priority = priority;
  p->ppid = running->pid;
  p->parent = running;
  // set kstack to resume to body
  // stack = r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r14
  //         1  2  3  4  5  6  7  8  9  10 11  12  13  14
  for (i=1; i<15; i++)
      p->kstack[SSIZE-i] = 0;
  p->kstack[SSIZE-14] = p->pid;
  p->kstack[SSIZE-13] = p->ppid;
  p->kstack[SSIZE-12] = func;
  p->kstack[SSIZE-11] = priority;

  p->kstack[SSIZE-1] = (int)func;  // in dec reg=address ORDER !!!

  p->ksp = &(p->kstack[SSIZE-14]);

  enqueue(&readyQueue, p);
  printf("%d kforked a child %d\n", running->pid, p->pid);
  printList("readyQueue", readyQueue);

  if (q){
      while(q->sibling)
          q=q->sibling;
      q->sibling = p;
  }
  else{
      running->child = p;
  }

  kprintf("Child list: ");
  q = running->child;
  while(q){
    kprintf("\n %d %d ", q->pid, q->priority);
    q = q->sibling;
  }
  kprintf("\n");

  return p;
}

int ksleep(int event)
{
    int SR = int_off();//disable IRQ and return CPSR
    running->event = event;
    running->status = SLEEP;
    tswitch();//switch process
    int_on(SR);
}

int kwakeup(int event)
{
    int SR = int_off();
    //PROC *p = &proc[1];//let p = p1
    int i;
    PROC *p;
    for (i=1;i<NPROC;i++){
        p = &proc[i];
        if(p->status == SLEEP && p->event == event){
            p->event = 0;
            p->status = READY;
            enqueue(&readyQueue, p);
        }
    }
   int_on(SR);
}

void kexit(int exitValue)
{
  PROC *p1 = &proc[1];// p1 == P1
  int HaveChild=0;
  if (running->pid == 1){// P1 never dies;
    kprintf("P1 never dies!!");
    return;
  }
  if(running->child){
    HaveChild = 1;
    p1 = p1->child;
    while(p1->sibling)
        p1 = p1->sibling;
    p1->sibling = running->child;//give away children to P1
    p1 = p1->sibling;
    running->child = 0;
    p1->ppid = (&proc[1])->pid;
    p1->parent = &proc[1];
  }
  p1 = &proc[1];//reset to P1

  running->exitCode = exitValue;//record exitValue in caller's PROC.exitCode
  printf("proc %d kexit\n", running->pid);
  //running->status = FREE;
  running->status = ZOMBIE;
  running->priority = 0;

  if(HaveChild)
      if(p1->status == SLEEP)
          kwakeup(&proc[1]);
  kwakeup(running->parent);

  //enqueue(&freeList, running);   // putproc(running);
  tswitch();
}

int ReleaseZombie(PROC *p)
{
    p->status = FREE;
    enqueue(&freeList, p);
}

int kwait(int *status)
{
    PROC *temp = running;
    if(running->child == 0)
        return -1;
    if(temp->child->status == ZOMBIE){
        status = temp->child->exitCode;
        running->child = temp->child->sibling;
        temp->sibling->parent = running;

        ReleaseZombie(temp);
        return temp->child->pid;
    }
    while(temp->sibling){
        if(temp->sibling->status == ZOMBIE){
            *status = temp->sibling->exitCode;
            temp->sibling = temp->sibling->sibling;
            ReleaseZombie(temp->sibling);
            return temp->sibling->pid;
        }
        temp = temp->sibling;
    }
    ksleep(running);

}

int scheduler()
{
  kprintf("proc %d in scheduler ", running->pid);
  if (running->status == READY)
      enqueue(&readyQueue, running);
  running = dequeue(&readyQueue);
  kprintf("next running = %d\n", running->pid);
}

void do_exit()
{
    int c;
    char exit_code[50];
    int i;
    kprintf("Enter exit code: ");
    /***
    c = kgetc();
    while(c != 'r'){
        kprintf("%c", c);
        exit_code[i++] = c;
        c = kgetc();
    }
    exit_code[i] = '\r';
    ***/
    kexit(geti(exit_code));
}

void do_wait()
{
    int status;
    int pid = kwait(&status);
    if (pid == -1)
        kprintf("Don't have child, exit_code: %d\n", status);
    else
        kprintf("ZOMBIE child pid: %d, exit_code: %d\n", pid, status);
}


int body(int pid, int ppid, int func, int priority)
{
  char c; char line[64];
  PROC *q = running->child;
  kprintf("proc %d resume to body()\n", running->pid);
  while(1){
    pid = running->pid;
    if (pid==0) color=BLUE;
    if (pid==1) color=WHITE;
    if (pid==2) color=GREEN;
    if (pid==3) color=CYAN;
    if (pid==4) color=YELLOW;
    if (pid==5) color=WHITE;
    if (pid==6) color=GREEN;
    if (pid==7) color=WHITE;
    if (pid==8) color=CYAN;

    printList("readyQueue", readyQueue);
    kprintf("proc %d running, parent = %d  ", running->pid, running->ppid);

    kprintf("\npid = %d", pid);
    kprintf("\nppid = %d", ppid);
    kprintf("\nfunc = %x", func);
    kprintf("\npriority = %d", priority);

    kprintf("\nchild list:");
    q = running->child;
    while(q){
        kprintf("[%d %d] ", q->pid, q->priority);
        q = q->sibling;
    }
    kprintf("\n");


/***    if(temp)
    while(temp)
    {
        kprintf("%d, ", temp->pid);
        temp = temp->sibling;
    }
    else
        kprintf("NULL");
    kprintf("\n");
***/

    kprintf("input a char [s|f|q|w] : ");
    c = kgetc();
    printf("%c\n", c);

    switch(c){
      case 's': tswitch();           break;
      case 'f': kfork((int)body, 1); break;
      case 'q': do_exit();           break;
      case 'w': do_wait();           break;
    }
  }
}


