#include <iostream>
#include <sstream>
#include <vector>
#include <memory>
#include "minisat/core/Solver.h"

using namespace std;
using namespace Minisat;

void vertexCover(vector<vector<int>> E, int v) {
    if (E.empty())
        return;

    for (int m = 1; m < v; ++m) {
        unique_ptr<Solver> solver(new Solver());
        vector<vector<Lit>> lit(v);

        //initialize
        for (int i = 0; i < v; ++i)
            for (int j = 0; j < m; ++j) {
                Lit l = mkLit(solver->newVar());
                lit[i].push_back(l);
            }

        //At least one vertex is the ith vertex in the vertex cover.
        for (int i = 0; i < m; ++i) {
            vec<Lit> ps;
            for (int j = 0; j < v; ++j) {
                ps.push(lit[j][i]);
            }
            solver->addClause(ps);
        }

        //No one vertex can appear twice in a vertex cover.
        for (int i = 0; i < v; ++i)
            for (int j = 0; j < m - 1; ++j)
                for (int k = j + 1; k < m; ++k)
                    solver->addClause(~lit[i][j], ~lit[i][k]);

        //No more than one vertex appears in the mth position of the vertex cover.
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < v - 1; ++j)
                for (int k = j + 1; k < v; ++k)
                    solver->addClause(~lit[j][i], ~lit[k][i]);

        //Every edge is incident to at least one vertex in the vertex cover.
        for (unsigned i = 0; i < E.size(); ++i) {
            vec<Lit> ps;
            for (int j = 0; j < m; ++j) {
                ps.push(lit[E[i][0]][j]);
                ps.push(lit[E[i][1]][j]);
            }
            solver->addClause(ps);
        }

        if (solver->solve()) {
            vector<int> res;
            for (int i = 0; i < v; ++i)
                for (int j = 0; j < m; ++j)
                    if (solver->modelValue(lit[i][j]) == l_True)
                        res.push_back(i);
            for (unsigned i = 0; i < res.size(); ++i) {
                if (i == 0)
                    cout << res[i];
                else
                    cout << " " << res[i];
            }
            cout << endl;
            solver.reset(new Solver());
            return;
        }
        solver.reset(new Solver());
    }
}

void parseLine(string &line, int &v) {
    stringstream input(line);
    char cmd;
    input >> cmd;

    if (input.fail())
        return;

    if (cmd == 'V') {
        input >> v;
    } else if (cmd == 'E') {
        vector<vector<int>> E;
        while (!input.eof()) {
            char symbol;
            input >> symbol;
            if (symbol == '<') {
                int vertex1, vertex2;
                char comma;
                input >> vertex1 >> comma >> vertex2;
                E.push_back({vertex1, vertex2});
            }
        }
        vertexCover(E, v);
    }
}

int main() {
    int v;
    while (!cin.eof()) {
        string line;
        getline(cin, line);
        parseLine(line, v);
    }
    return 0;
}
