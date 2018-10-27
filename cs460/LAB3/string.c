int strlen(char *s)
{
    int i=0;
    while(*(s++))
        i++;
    return i;
}

int strcmp(char *s1, char *s2)
{
    while(*s1==*s2)
        if(*(s1++)!=*(s2++))
            return 1;
    return 0;
}

int strcpy(char *dest, char *src)
{
    while(*src)
        *(dest++) = *(src++);
}

int strncpy(char *dest, char *src, int n)
{
    for(;n>=0;n--)
        if(*(src+n))
            *(dest+n) = *(src+n);
        else
            *(dest+n) = 0;
}

int strncmp(char *s1, char *s2, int n)
{
    for(;n>=0;n--)
        while(*s1==*s2)
            if(*(s1+n)!=*(s2+n))
                return 1;
    return 0;
}

int memcpy(char *dest, char *src, int n)
{
    if (dest <= src ||(char *)dest >= (char *)src + n)
        while(n--)
        {
            *(char *)dest = *(char *)src;
            dest = (char *)dest + 1;
            src = (char *)src + 1;
        }
    else
    {
        src = (char *)src + n -1;
        dest = (char *)dest + n -1;
        while (n--)
        {
            *(char *)dest = *(char *)src;
            dest = (char *)dest - 1;
            src = (char *)src - 1;
        }
    }
    return 1;
}

int memset(char *dest, char c, int n)
{
    while (n--)
    {
        *(char *)dest = (char)c;
        dest = (char *)dest +1;
    }
    return 1;
}

