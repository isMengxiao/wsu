
// queue.c file
extern PROC *freeList;
extern TPROC *timeQueue;
extern int kprintf(char *fmt, ...);
// WRITE YOUR OWN functions:

int enqueue(PROC **queue, PROC *p)
{
    int SR = int_off();  // IRQ interrupts off, return CPSR
    PROC *temp;
    temp = *queue;
    if (temp)
    {
        if(temp->priority < p->priority){
            p->next = temp;
            *queue = p;
        }
        else{
            while(temp->next &&(temp->next->priority >= p->priority))
                temp = temp->next;
            p->next = temp->next;
            temp->next = p;
        }
    }
    else
    {
        *queue = p;
    }
    //enter p into *queue by priority; PROCs with the same priority by FIFO;
    int_on(SR);          //  restore CPSR
}
PROC *dequeue(PROC **queue)
{
    int SR = int_off();  // IRQ interrupts off, return CPSR
    PROC *dequeued;
    dequeued = *queue;
    *queue = (*queue)->next;//remove the FISRT element from *queue;
    int_on(SR);          //  restore CPSR
    dequeued->next = 0;
    return dequeued;//pointer to dequeued PROC;
}


int printList(char *name, PROC *p)
{
    kprintf("%s = ", name);
    while(p){
        kprintf("[%d%d]->", p->pid, p->priority);
        p = p->next;
    }
    kprintf("NULL\n");
}

