#include <iostream>
#include <vector>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>

using namespace std;

int main(int argc, char **argv) {
    vector<pid_t> kids;

    int rgen_a1[2];
    int a1_a2[2];
    pipe(rgen_a1);
    pipe(a1_a2);

    pid_t child_pid;
    child_pid = fork();
    if (child_pid == 0) {
        dup2(rgen_a1[1], STDOUT_FILENO);
        close(rgen_a1[0]);
        close(rgen_a1[1]);
        return execv("./rgen", argv);
    } else if (child_pid < 0) {
        cerr << "Error: could not fork."<<endl;
        return 1;
    }
    kids.push_back(child_pid);

    child_pid = fork();
    if (child_pid == 0) {
        dup2(rgen_a1[0], STDIN_FILENO);
        close(rgen_a1[1]);
        close(rgen_a1[0]);

        dup2(a1_a2[1], STDOUT_FILENO);
        close(a1_a2[0]);
        close(a1_a2[1]);


        char *runPy[3] = {(char *) "python", (char *) "ece650-a1.py", nullptr};
        return execvp("python", runPy);
    } else if (child_pid < 0) {
        cerr << "Error: could not fork."<<endl;
        return 1;
    }
    kids.push_back(child_pid);

    child_pid = fork();
    if (child_pid == 0) {
        dup2(a1_a2[0], STDIN_FILENO);
        close(a1_a2[1]);
        close(a1_a2[0]);
        return execv("./ece650-a2", argv);
    } else if (child_pid < 0) {
        cerr << "Error: could not fork." << endl;
        return 1;
    }
    kids.push_back(child_pid);

    dup2(a1_a2[1], STDOUT_FILENO);
    close(a1_a2[0]);
    close(a1_a2[1]);
    while (!cin.eof()) {
        string line;
        getline(cin, line);
        cout << line << endl;
    }
    for (pid_t k:kids) {
        int status;
        kill(k, SIGTERM);
        waitpid(k, &status, 0);
    }
    return 0;
}
