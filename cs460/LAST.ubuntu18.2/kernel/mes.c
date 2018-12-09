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
