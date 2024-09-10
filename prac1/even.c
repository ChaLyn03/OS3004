#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h> // Include this for signal handling

// Signal handler for SIGHUP
void handle_sighup(int signum) {
    printf("Ouch!\n");
}

// Signal handler for SIGINT
void handle_sigint(int signum) {
    printf("Yeah!\n");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);

    // Set up signal handlers
    signal(SIGHUP, handle_sighup);
    signal(SIGINT, handle_sigint);

    for (int i = 0, count = 0; count < n; i++) {
        if (i % 2 == 0) {
            printf("%d\n", i);
            sleep(5);
            count++;
        }
    }

    return 0;
}
