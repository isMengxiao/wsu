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
#include "type.h"
#include "string.c"
#include "queue.c"
char *tab = "0123456789ABCDEF";
int color;

#include "timer.c"
#include "vid.c"


#include "interrupts.c"
#include "kernel.c"
#include "kbd.c"
#include "uart.c"
#include "pipe.c"
PIPE *kpipe;
//#include "exceptions.c"
UART *up = &uart[0];

int pipe_writer()
{
    char line[128];
    while(1){
        uprintf("Enter a line for task1 to get:");
        kprintf("task%d waits for line from UART0\n", running->pid);
        tswitch();
        ugets(up, line);
        uprints(up, "\r\n");
        kprintf("task%d writes line=[%s] to pipe\n", running->pid, line);
        write_pipe(kpipe, line, strlen(line));
    }
}
int pipe_reader()
{
    char line[128];
    int i, n;
    while(1){
        kprintf("task%d reading from pipe\n", running->pid);
        n = read_pipe(kpipe, line, 20);
        kprintf("task%d read n=%d bytes from pip3: [", running->pid, n);
        for (i=0; i<n; i++)
            kputc(line[i]);
        kprintf("]\n");
    }
}

void copy_vectors(void) {
    extern u32 vectors_start;
    extern u32 vectors_end;
    u32 *vectors_src = &vectors_start;
    u32 *vectors_dst = (u32 *)0;

    while(vectors_src < &vectors_end)
       *vectors_dst++ = *vectors_src++;
}
int kprintf(char *fmt, ...);

void timer_handler();
void kbd_handler();
void uart_handler();

int timer_task()
{
    int i;
    TIMER *t = &timer[8];
    while(1){
        printf("timer_task %d running\n", running->pid);
        ksleep((int)&timer);
        t->clock[7]='0'+(t->ss%10); t->clock[6]='0'+(t->ss/10);
        t->clock[4]='0'+(t->mm%10); t->clock[3]='0'+(t->mm/10);
        t->clock[1]='0'+(t->hh%10); t->clock[0]='0'+(t->hh/10);

        for (i=0; i<8; i++){
            kpchar(t->clock[i], 0, 70+i);
        }

    }
}
int uart_task()
{
    char line[128];
    kprintf("test uart");
    while(1){
        uprintf("uart_task %d sleep for line from UART\n", running->pid);
        ksleep((int)&uart[0]);
        uprintf("uart_task %d running\n", running->pid);
        ugets(up,line);
        uprintf("line = %s\n", line);
    }
}

int kbd_task()
{
    char line[128];
    while(1){
        printf("KBD task %d sleep for a line from KBD\n", running->pid);
        ksleep((int)&kbd);
        printf("KBD task %d running\n", running->pid);
        kgets(line);
        printf("line = %s\n", line);
    }
}

// IRQ interrupts handler entry point
// void __attribute__((interrupt)) IRQ_handler()
// timer0 base=0x101E2000; timer1 base=0x101E2020
// timer3 base=0x101E3000; timer1 base=0x101E3020
// currentValueReg=0x04
TIMER *tp[4];
/***
//extern int getcpsr();
//extern int getspsr();
void showregister(){
    int cpsr = getcpsr();
    int spsr = getspsr();
    int mode = cpsr & 0b11111;
    int premode = spsr & 0b11111;
    if (mode == 0b10011)
        kprintf("CPU is in the SVC mode!\n\r");
    else if (mode == 0b10010){
        if(premode == 0b10011)
            kprintf("CPU is in the IRQ mode, previous Mode is SVC mode .\n\r");
        else
            kprintf("CPU is in the IRQ mode, previous Mode is IRQ mode .\n\r");
    }

}
***/
int show =1;
void IRQ_handler()
{
    int vicstatus, sicstatus;
    int ustatus, kstatus;
    // read VIC SIV status registers to find out which interrupt
    vicstatus = VIC_STATUS;
    sicstatus = SIC_STATUS;
    // kprintf("vicstatus=%x sicstatus=%x\n", vicstatus, sicstatus);
    // VIC status BITs: timer0,1=4, uart0=13, uart1=14, SIC=31: KBD at 3
    /**************
    if (vicstatus & 0x0010){   // timer0,1=bit4
      if (*(tp[0]->base+TVALUE)==0) // timer 0
         timer_handler(0);
      if (*(tp[1]->base+TVALUE)==0)
         timer_handler(1);
    }
    if (vicstatus & 0x0020){   // timer2,3=bit5
       if(*(tp[2]->base+TVALUE)==0)
         timer_handler(2);
       if (*(tp[3]->base+TVALUE)==0)
         timer_handler(3);
    }
    if (vicstatus & 0x80000000){
       if (sicstatus & 0x08){
          kbd_handler();
       }
    }
    *********************/
    /**********
    if (vicstatus & (1<<4)){   // timer0,1=bit4
      if (*(tp[0]->base+TVALUE)==0) // timer 0
         timer_handler(0);
      if (*(tp[1]->base+TVALUE)==0)
         timer_handler(1);
    }
    if (vicstatus & (1<<5)){   // timer2,3=bit5
       if(*(tp[2]->base+TVALUE)==0)
         timer_handler(2);
       if (*(tp[3]->base+TVALUE)==0)
         timer_handler(3);
    }
    *****************/
    if (vicstatus & (1<<4))   // timer0,1=bit4
         timer_handler(0);

    if (vicstatus & (1<<12))
        uart_handler(&uart[0]);

    if (vicstatus & (1<<31))
      if (sicstatus & (1<<3))
          kbd_handler();
    /***
    if (show)
    {
        showregister();
        show = 0;
    }
    ***/
}
int main()
{
   int i;
   char line[128];
   KBD *kp;
   UART *up;

   color = YELLOW;
   row = col = 0;
   fbuf_init();

   /* enable timer0,1, uart0,1 SIC interrupts */
   VIC_INTENABLE |= (1<<4);  // timer0,1 at bit4
   VIC_INTENABLE |= (1<<5);  // timer2,3 at bit5

   VIC_INTENABLE |= (1<<12);
   VIC_INTENABLE |= (1<<13);
   VIC_INTENABLE |= (1<<31); // SIC to VIC's IRQ31

   /* enable KBD IRQ */
   SIC_ENSET = 1<<3;     // KBD int=3 on SIC
   SIC_PICENSET = 1<<3;  // KBD int=3 on SIC

   //timer_init();
   uart_init();
   kbd_init();
   pipe_init();
   /***************
   for (i=0; i<4; i++){
      tp[i] = &timer[i];
      timer_start(i);
   }
   ************/
   kpipe = create_pipe();
  // kernel_nit();
   up = &uart[0];
   kp = &kbd;
   //timer_start(0);
   init();
   printf("P0 create tasks\n");
   //kfork((int)timer_task, 3);
   kfork((int)pipe_writer,  1);
   kfork((int)pipe_reader,   1);
   while(1){
       if(readyQueue)
           tswitch();
   }
}
