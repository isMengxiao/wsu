/*********************** t.c file ***************************/
#include "../type.h"
int main()
{
    fbuf_init();
    //initialize LCD frame buffer: driver/vid.c
    printf("Welcome to WANIX in Arm\n");
    binit();
    // I/O buffers: fs/buffer.c
    vectorInt_init(); // Vectored Interrupts: driver/int.c
    irq_init(); // Configure VIC,SIC,deviceIRQs: driver/int.c
    kbd_init(); // Initialize KBB driver: driver/kbd.c
    uart_init(); // initialize UARTs:driver/uart.c
    timer_init(); // initialize timer:driver/timer.c
    timer_start(0);// start timer0driver/timer.c
    sdc_init();   // initialize SDC driver: driver/sdc.c
    kernel_init(); // initialize kernel structs:kernel/kernel.c
    fs_init(); // initialize FS and mount root file system
    kfork("/bin/init"); // create INIT proc P1: kernel/fork.c
    printf("P0 switch to P1\n");
    while(1){
        // P0 code
        while(!readyQueue); // loop if no runnable procs
        tswitch();
    }
}
int scheduler()
{
    PROC *old = running;
    if (running->pid == 0 && running->status == BLOCK){// P0 only
        unlock();
        while(!readyQueue);
        return;
    }
    if (running->status==READY)
        enqueue(&readyQueue, running);
    running = dequeue(&readyQueue);
    if (running != old){
        switchPgdir((int)running->res->pgdir);
    }
    running->time = 10; // time slice = 10 ticks;
    sw_flag = 0;
    // turn off switch task flag
}
int schedule(PROC *p)
{
    if (p->status ==READY)
        enqueue(&readyQueue, p);
    if (p->priority > running->priority)
        sw_flag = 1;
}
int reschedule()
{
    if (sw_flag)
        tswitch();
}
