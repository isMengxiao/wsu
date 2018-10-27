#define NPIPE 9
#define PSIZE 8
#define FREE  0
#define BUSY  1

typedef struct pipe{
    char buf[PSIZE];
    int head, tail;
    int data, room;
    int status;
}PIPE;

PIPE pipe[NPIPE];
int pipe_init()
{
    printf("pipe_init()\n");
    int i;
    for(i=0; i<NPIPE; i++){
        pipe[i].status = FREE;
    }
}

PIPE *create_pipe()
{
    PIPE *temp;
    temp = &pipe[0];
    temp->head = 0;
    temp->tail = 0;
    temp->data = 0;
    temp->room = PSIZE;
    temp->status = BUSY;
    return temp;
}
//---------- Algorithm of pipe_read-------------
int read_pipe(PIPE *p, char *buf, int n)
{
    kprintf("pipe reader:%d ", n);
    int r = 0;
    if (n<=0)
        return 0;
    //validate PIPE pointer p;
    if(p->status==FREE)
        return -1;
    while(n){
        while(p->data){
            *buf++ = p->buf[p->tail++]; 	// read a byte to buf
            p->tail %= PSIZE;
            p->data--; p->room++; r++; n--;
            if (n==0) break;
        }
        kwakeup(&p->room);
        if(r)
            return r;
        ksleep(&p->data);
    }
}

//---------- Algorithm of write_pipe -----------
int write_pipe(PIPE *p, char *buf, int n)
{
    int r = 0;
    if (n<=0){
        return 0;}
    //validate PIPE pointer p;
    if(p->status==FREE)
        return -1;
    while(n){printf("writer print n: %d", n);
        while(p->room){
            p->buf[p->head++] = *buf++; 	// write a byte to pipe;
            p->head %= PSIZE;
            p->data++; p->room--; r++; n--;
            if (n==0) {
                break;}
        }
        kwakeup(&p->data);
        if(n==0)
            return r;
        ksleep(&p->room);
    }
}
