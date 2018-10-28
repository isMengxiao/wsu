
int strlen(char *s)
{
}

int strcmp(char *s1, char *s2)
{
}

int strcpy(char *dest, char *src)
{
}

int strcat(char *dest, char *src)
{
}

int atoi(char *s)
{
  int v = 0;
  while (*s){
    v = 10*v + (*s - '0');
    s++;
  }
  return v;
}
int geti()
{
  char s[16];
  kgetline(s);
  return atoi(s);
}

int memcpy(char *dest, char *src, int size)
{
}
