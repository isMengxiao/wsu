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

//char *tab = "0123456789ABCDEF";
#define DR   0x00
#define UDS  0x04
#define FR   0x18
#define CNTL 0x2C
#define IMSC 0x38
#define MIS  0x40
#define SBUFSIZE 128

typedef volatile struct uart{
  char *base;           // base address
  int  n;
  char inbuf[SBUFSIZE];
  int indata, inroom, inhead, intail;
  char outbuf[SBUFSIZE];
  int outdata, outroom, outhead, outtail;
  volatile int txon;//1=TX interrupt is on
}UART;

UART uart[4];  // 4 UART structs

int uart_init()
{
  int i;
  UART *up;
  for (i=0; i<4; i++){
    up = &uart[i];
    up->base = (char *)(0x101f1000 + i*0x1000);
    *(up->base + CNTL) &= ~0x10;
    *(up->base + IMSC) |= 0x30;
    up->n = i;
    up->indata = up->inhead = up->intail = 0;
    up->inroom = SBUFSIZE;
    up->outdata = up->outhead = up->outtail = 0;
    up->outroom = SBUFSIZE;
    up->txon = 0;
  }
  uart[3].base = (char *)(0x10009000);
}

void uart_handler(UART *up)
{
    u8 mis = *(up->base + MIS);
    if (mis & (1<<4))
        do_rx(up);
    if (mis & (1<<5))
        do_tx(up);
}
int do_rx(UART *up)
{
    char c;
    c = *(up->base + DR);
    //printf("rx interrupt: %c\n", c);
    if (c == 0xD)
        printf("\n");
    up->inbuf[up->inhead++] = c;
    up->inhead %= SBUFSIZE;
    up->indata++;
    up->inroom--;
    kwakeup(up);
}
int do_tx(UART *up)
{
    char c;
    //printf("TX interrupt\n");
    if (up->outdata <= 0){
        *(up->base + IMSC) = 0x10;
        up->txon = 0;
        return;
    }
    c = up->outbuf[up->outtail++];
    up->outtail %= SBUFSIZE;
    *(up->base + DR) = (int)c;
    up->outdata--;
    up->outroom++;
}

int uputc(UART *up, char c)
{
    //kprintf("uputc %c ", c);
    if (up->txon){
        up->outbuf[up->outhead++] = c;
        up->outhead %= 128;
        lock();
        up->outdata++;
        up->outroom--;
        unlock();
        return;
    }
    int i = *(up->base + FR);
    while( *(up->base + FR) & 0x20 );
    *(up->base + DR) = (int)c;
    UART0_IMSC |= 0x30;
    up->txon = 1;
}

int ugetc(UART *up)
{
    char c;
    while(up->indata <= 0);
        c = up->inbuf[up->intail++];
    up->intail %= SBUFSIZE;
    lock();
    up->indata--;
    up->inroom++;
    unlock();
    return c;
}

int ugets(UART *up, char *s)
{
    kprintf("%s", "in ugets: ");
    while ((*s = (char)ugetc(up)) != '\r'){
        uputc(up, *s++);
  }
 *s = 0;
}

int uputs(UART *up, char *s)
{
  while(*s){
    uputc(up, *s++);
    if (*s=='\n')
      uputc(up,'\r');
  }
}

int uprints(UART *up, char *s)
{
  while(*s)
    uputc(up, *s++);
}

int urpx(UART *up, int x)
{
  char c;
  if (x){
     c = tab[x % 16];
     urpx(up, x / 16);
  }
  uputc(up, c);
}

int uprintx(UART *up, int x)
{
  uprints(up, "0x");
  if (x==0)
    uputc(up, '0');
  else
    urpx(up, x);
  uputc(up, ' ');
}

int urpu(UART *up, int x)
{
  char c;
  if (x){
     c = tab[x % 10];
     urpu(up, x / 10);
  }
  uputc(up, c);
}

int uprintu(UART *up, int x)
{
  if (x==0)
    uputc(up, '0');
  else
    urpu(up, x);
  uputc(up, ' ');
}

int uprinti(UART *up, int x)
{
  if (x<0){
    uputc(up, '-');
    x = -x;
  }
  uprintu(up, x);
}

int ufprintf(UART *up, char *fmt,...)
{
  int *ip;
  char *cp;
  cp = fmt;
  ip = (int *)&fmt + 1;

  while(*cp){
    if (*cp != '%'){
      uputc(up, *cp);
      if (*cp=='\n')
	uputc(up, '\r');
      cp++;
      continue;
    }
    cp++;
    switch(*cp){
    case 'c': uputc(up, (char)*ip);      break;
    case 's': uprints(up, (char *)*ip);  break;
    case 'd': uprinti(up, *ip);           break;
    case 'u': uprintu(up, *ip);           break;
    case 'x': uprintx(up, *ip);  break;
    }
    cp++; ip++;
  }
}

int uprintf(char *fmt, ...)
{
  int *ip;
  char *cp;
  cp = fmt;
  ip = (int *)&fmt + 1;

  UART *up = &uart[0];

  while(*cp){
    if (*cp != '%'){
      uputc(up, *cp);
      if (*cp=='\n')
	    uputc(up, '\r');
      cp++;
      continue;
    }
    cp++;
    switch(*cp){
    case 'c': uputc(up, (char)*ip);      break;
    case 's': uprints(up, (char *)*ip);   break;
    case 'd': uprinti(up, *ip);           break;
    case 'u': uprintu(up, *ip);           break;
    case 'x': uprintx(up, *ip);  break;
    }
    cp++; ip++;
  }
}

