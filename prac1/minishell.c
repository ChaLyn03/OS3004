#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

<<<<<<< HEAD
#define NV 20          /* max number of command tokens */
#define NL 100         /* input buffer size */
char line[NL]; /* command input buffer */

int job_count = 0;   /* keeps track of the background job number */
int job_id = 1;      /* keeps track of the current job ID */

typedef struct Job {
    int job_id;
    pid_t pid;
    char command[NL];
    struct Job *next;
} Job;

Job *job_list = NULL;

void add_job(pid_t pid, char *command) {
    Job *new_job = (Job *)malloc(sizeof(Job));
    new_job->job_id = job_id++;
    new_job->pid = pid;
    strncpy(new_job->command, command, NL);
    new_job->next = job_list;
    job_list = new_job;
}

void remove_job(pid_t pid) {
    Job *prev = NULL;
    Job *current = job_list;

    while (current != NULL) {
        if (current->pid == pid) {
            if (prev == NULL) {
                job_list = current->next;
            } else {
                prev->next = current->next;
            }
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

void check_background_processes() {
    int status;
    pid_t pid;

    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        Job *job = job_list;
        while (job != NULL) {
            if (job->pid == pid) {
                printf("[%d]+ Done %s\n", job->job_id, job->command);
                remove_job(pid);
                break;
            }
            job = job->next;
        }
    }
=======
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
>>>>>>> f88bcbad5f8d15f5390c1685dfef01ac976c8beb
}

int main(int argk, char *argv[], char *envp[])
{
<<<<<<< HEAD
    int frkRtnVal;     /* value returned by fork sys call */
    int wpid;          /* value returned by wait */
    char *v[NV];       /* array of pointers to command line tokens */
    char *sep = " \t\n";/* command line token separators */
    int i;             /* parse index */
    int background;    /* flag for background processes */

    while (1) {
        // Prompt is disabled as per the instructions
        fgets(line, NL, stdin);

        if (feof(stdin)) {
            exit(0);
        }

        if (line[0] == '#' || line[0] == '\n' || line[0] == '\000')
            continue;
=======
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
>>>>>>> f88bcbad5f8d15f5390c1685dfef01ac976c8beb

        v[0] = strtok(line, sep);
        for (i = 1; i < NV; i++) {
            v[i] = strtok(NULL, sep);
            if (v[i] == NULL)
                break;
        }

<<<<<<< HEAD
        /* Check if the command should be run in the background */
        if (strcmp(v[i-1], "&") == 0) {
            background = 1;
            v[i-1] = NULL;  // Remove the '&' from the command arguments
=======
        /* check if the command should be run in the background */
        if (strcmp(v[i-1], "&") == 0) {
            background = 1;
            v[i-1] = NULL;  // remove the '&' from the command arguments
>>>>>>> f88bcbad5f8d15f5390c1685dfef01ac976c8beb
        } else {
            background = 0;
        }

<<<<<<< HEAD
        /* Handle the 'cd' command */
=======
        /* handle the 'cd' command */
>>>>>>> f88bcbad5f8d15f5390c1685dfef01ac976c8beb
        if (strcmp(v[0], "cd") == 0) {
            if (v[1] == NULL) {
                fprintf(stderr, "cd: expected argument\n");
            } else if (chdir(v[1]) != 0) {
<<<<<<< HEAD
                perror("chdir");
            }
            continue;
        }

        /* Fork a child process to exec the command in v[0] */
        frkRtnVal = fork();
        if (frkRtnVal < 0) {
            perror("fork failed");
            continue;
        }
        if (frkRtnVal == 0) { /* Child process */
            execvp(v[0], v);
            perror("execvp failed");
            exit(EXIT_FAILURE);
        }

        if (background) { /* Background process */
            printf("[%d] %d\n", job_id, frkRtnVal);
            add_job(frkRtnVal, v[0]);
        } else { /* Foreground process */
            wpid = waitpid(frkRtnVal, NULL, 0);
            if (wpid == -1) {
                perror("waitpid failed");
            }
            check_background_processes(); // Check and print any completed background processes
        }

        /* After every command input, check for any completed background processes */
        check_background_processes();
    }

    return 0;
}
=======
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
>>>>>>> f88bcbad5f8d15f5390c1685dfef01ac976c8beb
