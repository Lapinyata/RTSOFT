#include <unistd.h>
#include <stdio.h>
#define O_RDONLY         00
int main(){
    int fd = open("/dev/test", O_RDONLY);
    while(666) {
        unsigned int t = 38;
        unsigned int t2 = 573;
        t2 = read(fd, &t, sizeof(t));
        printf("%d\n", t2);
        sleep(1);
    }
}
