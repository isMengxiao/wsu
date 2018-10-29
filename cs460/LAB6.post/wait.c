int ksleep(int event)
{
  int sr = int_off();
  printf("proc %d ksleep on %x\n", running->pid, event);
  running->event = event;
  running->status = SLEEP;
  enqueue(&sleepList, running);
  printf("sleepList = "); printQ(sleepList);
  tswitch();
  int_on(sr);
}

int kwakeup(int event)
{
  PROC *p, *tmp=0;
  int sr = int_off();
  while((p = dequeue(&sleepList))!=0){
    if (p->event==event){
      printf("kwakeup %d\n", p->pid);
      p->status = READY;
      enqueue(&readyQueue, p);
    }
    else{
      enqueue(&tmp, p);
    }
  }
  sleepList = tmp;
  int_on(sr);
}

int kexit(int exitvalue)
{
    int i;
    int wk1;
    PROC *p;
    wk1 = 0;
        return -1;
///2.dispose of children process, if any
    for (i=1; i<NPROC; i++){
        p = &proc[i];
        if ((p->status != FREE) && (p->ppid == running->pid)){
            kprintf("give %d to P1\n", p->pid);
            p->ppid = 1;
            p->parent = &proc[1];
            wk1++;
        }
    }
///3. record exitValue in PROC.exitCode for parent to get.
    running->exitCode = exitvalue;
///4. become a ZOMBIE (but do not free the PROC)
    running->status   = ZOMBIE;
///5. wakeup parent and, if needed, also the INIT process P1.
    kwakeup((int)running->parent);
    if(wk1)
        kwakeup((int)&proc[1]);
///6. switch process to give up CPU
    tswitch();

}

int kwait(int *status)
{
    int i;
    int child = 0;
    PROC *p;

    for (i=1; i<NPROC; i++){
        p = &proc[i];
        if (p->status != FREE && p->ppid == running->pid){
            child++;
        }
    }
    if (child == 0){
        kprintf("no child\n");
        return -1;
    }

    while(1){
        for (i=1; i<NPROC; i++){
            p = &proc[i];
            if ((p->status == ZOMBIE) && (p->ppid == running->pid)){
                kprintf("found a ZOMBIe child %d\n", p->pid);
                *status = p->exitCode;
                p->status = FREE;
                enqueue(&freeList, p);
                return p->pid;
            }
        }
     //   kprintf("sleep on %x\n", running);
        ksleep((int)running);
    }
}



