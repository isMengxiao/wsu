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

int ksleep(int event)
{
  int SR = int_off();
  running->event = event;
  running->status = SLEEP;
  tswitch();
  int_on(SR);
}

int kwakeup(int event)
{
  int SR = int_off();printf("111");
  int i; PROC *p;
  for(i=1; i<NPROC; i++)
  {
     p = &proc[i];
     if(p->status == SLEEP && p->event == event){
          p->event=0;
          p->status = READY;
          enqueue(&readyQueue,p);
     }
  }
  int_on(SR);
}

int kwait(int *status)
{PROC *tmp=0;PROC *tmp1=0;
if(running->child == 0)
  {
    printf("wait error: no child\n");
    return -1; 
  }
  else
  { 
    if(running->child->status==ZOMBIE)  
    { 
      status = running->child->exitCode;
      tmp=running->child;
      running->child = running->child->sibling;
      enqueue(&freeList, tmp);
      return running->child->pid;
    }else{tmp = running->child;}
    while(1){
       if(tmp->sibling==0)break;
       else{
         if(tmp->sibling->status==ZOMBIE)
         {
           status = tmp->sibling->exitCode;
           tmp1=tmp->sibling;
           tmp->sibling=tmp->sibling->sibling;
           enqueue(&freeList, tmp1);
           return tmp->sibling->pid;
         }
         else
         {
           tmp=tmp->sibling;
         }
       }
    }
   ksleep(running); 
  }   
}

void kexit(exitValue)
{
  printf("proc %d in kexit():exitCode = %d\n", running->pid,exitValue);
  if(running->child!=0){PROC *p = &proc[1];p->child=running->child ;running->child=0;kwakeup(&proc[1]);}
  running->exitCode=exitValue;
  running->status = ZOMBIE;
  running->priority = 0;
  kwakeup(running->parent);
  //dequeue(&readyQueue);
  tswitch();
}
  
PROC *kfork(int func, int priority)
{
  int i;
  PROC *p = dequeue(&freeList);
  if (p==0){
    printf("no more PROC, kfork failed\n");
    return 0;
  }
  p->status = READY;
  p->priority = priority;
  p->ppid = running->pid;
  p->parent = running;
  if(running->child==0)running->child = p;
  else
  {
    PROC *tmp = running->child;
    while(tmp->sibling!=0)tmp=tmp->sibling; 
    tmp->sibling=p;
    p->sibling=0;  
  }
  // set kstack to resume to body
  // stack = r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r14
  //         1  2  3  4  5  6  7  8  9  10 11  12  13  14
  for (i=1; i<11; i++)
      p->kstack[SSIZE-i] = 0;


  p->kstack[SSIZE-1] = (int)func;  // in dec reg=address ORDER !!!
  p->ksp = &(p->kstack[SSIZE-14]);

  enqueue(&readyQueue, p);
  printf("%d kforked a child %d\n", running->pid, p->pid);
  return p;
}

int scheduler()
{
  if (running->status == READY)
      enqueue(&readyQueue, running);
  running = dequeue(&readyQueue);
  if (running->pid==1)
  kprintf("\nproc Producer running\n");
  else
  kprintf("\nproc Consumer running\n");  
}  


int body(int pid,int ppid, int func, int priority)
{
  char c; char line[64];
  kprintf("proc %d resume to body()\n", running->pid);
  while(1){
    if (running->pid==0) color=BLUE;
    if (running->pid==1) color=WHITE;
    if (running->pid==2) color=GREEN;
    if (running->pid==3) color=CYAN;
    if (running->pid==4) color=YELLOW;
    if (running->pid==5) color=WHITE;
    if (running->pid==6) color=GREEN;   
    if (running->pid==7) color=WHITE;
    if (running->pid==8) color=CYAN;
    
    printList("readyQueue", readyQueue);
    kprintf("proc %d running, parent = %d  ", running->pid, running->ppid);
    kprintf("input a char [f|s|q|w] : ");
    c = kgetc(); 
    printf("%c\n", c);
int status;
    switch(c){
      case 's': tswitch();           break;
      case 'f': kfork((int)body, 1); break;
      case 'q': if(running->pid==1) printf("P1 never die\n");
                else{
                printf("enter an exit value:");
                int exitValue = kgeti();
                printf("\n");
                kexit(exitValue); }            
                break;
      case 'w': pid = kwait(&status);break;
    }
  }
}
