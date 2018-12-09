typedef struct proc{
    struct proc *next;
    int *ksp;
    int *usp;
    int *upc;
    int *ucpsr;
    int status;
    int priority;
    int pid;
    int ppid;
    int event;
    int exitCode;
    int vforked;
    int time;
    int cpu;
    int type;
    int pause;
    struct proc *parent;
    struct proc *proc;
    struct pres *res;
    struct semaphore *sem;
    int *kstack;
}PROC;

typedef struct pres{
    int uid;
    int gid;
    u32 paddress, psize;
    u32 *pgdir;
    u32 *new_pgdir;
    MINODE *cwd;
    char name[32];
    char tty[32];
    int tcount;
    u32 signal;
    int sig[NSIG];
    OFT *fd[NFD];
    struct semaphore mlock;
    struct semaphore message;
    struct mbuf *mqueue;
}PRES;
