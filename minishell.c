#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

#define NV 20            /* max number of command tokens */
#define NL 100           /* input buffer size */
char line[NL];   /* command input buffer */


/*
    shell prompt
 */

void prompt(void)
{
    fprintf(stdout, "\n msh> ");
    fflush(stdout);
}

int main(int argk, char *argv[], char *envp[])
{
    int frkRtnVal;    /* value returned by fork sys call */
    int wpid;         /* value returned by wait */
    char *v[NV];    /* array of pointers to command line tokens */
    char *sep = " \t\n";/* command line token separators */
    int i;        /* parse index */
    int background;    /* flag for background processes */

    /* prompt for and process one command line at a time  */

    while (1) {            /* do Forever */
        prompt();
        fgets(line, NL, stdin);

        if (feof(stdin)) {        /* non-zero on EOF  */
            fprintf(stderr, "EOF pid %d feof %d ferror %d\n", getpid(),
                    feof(stdin), ferror(stdin));
            exit(0);
        }
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\000')
            continue;            /* to prompt */

        v[0] = strtok(line, sep);
        for (i = 1; i < NV; i++) {
            v[i] = strtok(NULL, sep);
            if (v[i] == NULL)
                break;
        }

        /* check if the command should be run in the background */
        if (strcmp(v[i-1], "&") == 0) {
            background = 1;
            v[i-1] = NULL;  // remove the '&' from the command arguments
        } else {
            background = 0;
        }

        /* handle the 'cd' command */
        if (strcmp(v[0], "cd") == 0) {
            if (v[1] == NULL) {
                fprintf(stderr, "cd: expected argument\n");
            } else if (chdir(v[1]) != 0) {
                perror("cd failed");
            }
            continue; /* continue to prompt */
        }

        /* fork a child process to exec the command in v[0] */

        frkRtnVal = fork();
        if (frkRtnVal < 0) {            /* fork returns error to parent process */
            perror("fork failed");
            continue;
        }
        if (frkRtnVal == 0) {            /* code executed only by child process */
            execvp(v[0], v);
            perror("execvp failed");
            exit(EXIT_FAILURE); /* terminate child process if exec fails */
        }

        if (!background) { /* parent waits if not a background process */
            wpid = wait(0);
            if (wpid == -1) {
                perror("wait failed");
            }
            printf("%s done \n", v[0]);
        } else { /* if background, notify when process finishes */
            printf("[%d] %s running in background\n", frkRtnVal, v[0]);
            signal(SIGCHLD, SIG_IGN); /* avoid zombies by ignoring SIGCHLD */
        }
    }                /* while */
    return 0;
}                /* main */
