************** mes.c file: Message Passing ************/
#include "../type.h"
/******** message buffer type in type.h ********
typedef struct mbuf{
struct mbuf *next;
int sender; // next mbuf pointer
// sender pid
int priority; // message priority
char text[128]; // message contents
} MBUF;
************************************************/
MBUF mbuf[NMBUF], *freeMbuflist;
// free mbufs; NMBUF=NPROC
SEMAPHORE mlock; // semaphore for exclusive access to mbuf[ ]
int mbuf_init()
{
    int i; MBUF *mp;
    printf("mbuf_init\n");
    for (i=0; i<NMBUF; i++){ // initialize mbufs
        mp = &mbuf[i];
        mp->next = mp+1;
        mp->priority = 1;
        // for enqueue()/dequeue()
    }
    freeMbuflist = &mbuf[0];
    mbuf[NMBUF-1].next = 0;
    mlock.value = 1; mlock.queue = 0;
}
MBUF *get_mbuf()
    // allocate a mbuf
{
    MBUF *mp;
    P(&mlock);
    mp = freeMbuflist;
    if (mp)
        freeMbuflist = mp->next;
    V(&mlock);
    return mp;
}
int put_mbuf(MBUF *mp)
    // release a mbuf
{
    mp->text[0] = 0;
    P(&mlock);
    mp->next = freeMbuflist;
    freeMbuflist = mp;
    V(&mlock);
}
int ksend(char *msg, int pid)
    // send message to pid
{
    MBUF *mp; PROC *p;
    // validate receiver pid
    if ( pid <= 0 || pid >= NPROC){
        printf("sendMsg : invalid target pid %d\n", pid);
        return -1;
    }
    p = &proc[pid];
    if (p->status == FREE || p->status == ZOMBIE){
        printf("invalid target proc %d\n", pid);
        return -1;
    }
    mp = get_mbuf();
    if (mp==0){
        printf("no more mbuf\n");
        return -1;
    }
    mp->sender = running->pid;
    strcpy(mp->text, msg);
    // copy text from Umode to mbuf
    // deliver mp to receiver's message queue
    P(&p->res->mlock);
    enqueue(&p->res->mqueue, mp);
    V(&p->res->mlock);
    V(&p->res->message);
    // notify receiver
    return 1;
}
int krecv(char *msg)
    // receive message from OWN mqueue
{
    MBUF *mp;
    P(&running->res->message);
    // wait for message
    P(&running->res->mlock);
    mp = (MBUF *)dequeue(&running->res->mqueue);
    V(&running->res->mlock);
    if (mp){
        // only if it has message
        strcpy(msg, mp->text); // copy message contents to Umode
        put_mbuf(mp);
        return 1; // release mbuf
    }
    return -1; // if proc was killed by signal => no message
}
