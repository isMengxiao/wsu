









//This is grep.c
#include "ucode.c"

int main(int argc, char* argv[])
{
    int fd=0, size, i;
    int line=0;
    char str[128];
    int signal=1;
    char *s;
    size = strlen(argv[1]);

    if (argc == 2){
        fd = dup(0);
    }
    else{
        fd = open(argv[2], O_RDONLY);
    }
    if (!fd)
        return 0;
    i = 0;
    while(signal){
        line++;
        while(i<128){
            signal = read(fd, &str[i], 1);
            if (!signal || str[i] == '\n' || str[i] == '\r'){
                str[i+1] = '\0';
                break;
            }
            i++;
        }

        s = str;
        while( *s != '\n'){
            if (!strncmp(s, argv[1], size) && str[0]){
                write(1, str, i+1);
                break;
            }
            s++;
        }
    }

}
//End of grep.c
