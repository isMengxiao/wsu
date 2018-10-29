
// queue.c file

extern PROC *freeList;

PROC *getproc()
{
  PROC *p = freeList;
  if (p){
    freeList = p->next;
  }
  return p;
}

int putproc(PROC *p)
{
  p->next = freeList;
  freeList = p;
}

int enqueue(PROC **queue, PROC *p)
{
  PROC *q  = *queue;
  if (q==0 || p->priority > q->priority){
    *queue = p;
    p->next = q;
    return;
  }
  while (q->next && p->priority <= q->next->priority){
    q = q->next;
  }
  p->next = q->next;
  q->next = p;
}

PROC *dequeue(PROC **queue)
{
  PROC *p = *queue;
  if (p)
    *queue = p->next;
  return p;
}

int printQ(PROC *p)
{
  kprintf("readyQueue = ");
  while(p){
    kprintf("[%d%d]->", p->pid,p->priority);
    p = p->next;
  }
  kprintf("NULL\n");
}

int printSleepList(PROC *p)
{
  printf("sleepList  = ");
   while(p){
     kprintf("[%d%d]->", p->pid,p->event);
     p = p->next;
  }
  kprintf("NULL\n");
}

int printList(PROC *p)
{
   kprintf("freeList   = ");
   while(p){
     kprintf("[%d]->", p->pid);
     p = p->next;
  }
  kprintf("NULL\n");
}
