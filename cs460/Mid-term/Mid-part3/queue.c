
// queue.c file
extern PROC *freeList;
// WRITE YOUR OWN functions:
int kprintf(char *fmt, ...);

int enqueue(PROC **queue, PROC *p)
{
  int SR = int_off();  // IRQ interrupts off, return CPSR
  //  enter p into *queue by priority; PROCs with the same priority by FIFO;
  PROC* tmp = *queue;
  if((*queue)==0) {*queue=p;}
  else
  if(p->priority>tmp->priority){p->next=tmp;*queue=p;}
  else
  {
    while( (tmp->next->priority >= p->priority) && (tmp->next != 0) )
	  tmp=tmp->next;
    p->next = tmp->next;
    tmp->next = p;
  }


  int_on(SR);          //  restore CPSR 
}				     

PROC *dequeue(PROC **queue)
{
  int SR = int_off();  // IRQ interrupts off, return CPSR
  //  remove the FISRT element from *queue; 
  /*PROC* tmp = *queue;
  int pp = (*queue)->pid;
  while(tmp->next->pid != pp)
	tmp=tmp->next;
  tmp->next=(*queue)->next;
  PROC* p = *queue;
  *queue=(*queue)->next;*/
  
  PROC* tmp = *queue;
  *queue=(*queue)->next;
  tmp->next=0;       
  int_on(SR);  //  restore CPSR 

  return tmp;
}

int printList(char *name, PROC *p)
{
   kprintf("%s = ", name);
   if(name == "child list")
   while(p){
     if(p->status==ZOMBIE)
     kprintf("[%d Z]->", p->pid );
else
kprintf("[%d R]->", p->pid );
     p = p->sibling;
  }else
   while(p){
     kprintf("[%d%d]->", p->pid, p->priority);
     p = p->next;
  }
  kprintf("NULL\n"); 
}

