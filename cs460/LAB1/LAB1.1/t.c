/*********  t.c file *********************/
int prints(char *s)
{
// write YOUR code
    while(*s)
    {
        putc(*(s++));
    }
    return 0;
}

int gets(char *s)
{
// write YOUR code
    while((*s = getc())!='\r')
    {
        putc(*(s++));
    }
    *s = '\0';

}

char ans[64];

main()
{
  while(1){
    prints("What's your name? ");
    gets(ans);  prints("\n\r");

    if (ans[0]==0){
      prints("return to assembly and hang\n\r");
      getc();
      return 0;
    }
    prints("Welcome "); prints(ans); prints("\n\r");
  }
}

