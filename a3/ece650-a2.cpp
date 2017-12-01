#include <iostream>
#include <sstream>
#include <vector>
#include <queue>

using namespace std;

struct CmdCheck {
    bool cmdV = false;
    bool cmdE = false;
};

struct Vertex {
    int prev = -1;
    int visit = 0;
};

bool parseLine(string line, char &cmd, CmdCheck &check, int vNum, vector<int> &data, string &errMsg) {
    stringstream input(line);
    input >> cmd;

    if (input.fail())
        return false;

    if (cmd == 'V') {
        if (check.cmdV) {
            errMsg = "Error: already have a valid V command.";
            return false;
        } else {
            int vertices;
            input >> vertices;
            data.push_back(vertices);
            check.cmdV = true;
            check.cmdE = false;
            return true;
        }
    } else if (cmd == 'E') {
        if (check.cmdE) {
            errMsg = "Error: already have a valid E command.";
            return false;
        } else {
            while (!input.eof()) {
                char symbol;
                input >> symbol;
                if (symbol == '<') {
                    int vertex1, vertex2;
                    char comma;
                    input >> vertex1 >> comma >> vertex2;
                    if (vertex1 >= vNum) {
                        errMsg = "Error: vertex " + to_string(vertex1) + " out of range.";
                        return false;
                    } else if (vertex2 >= vNum) {
                        errMsg = "Error: vertex " + to_string(vertex2) + " out of range.";
                        return false;
                    }
                    data.push_back(vertex1);
                    data.push_back(vertex2);
                }
            }
            check.cmdE = true;
            check.cmdV = false;
            return true;
        }
    } else if (cmd == 's') {
        int start, end;
        input >> start >> end;
        if (start >= vNum) {
            errMsg = "Error: vertex " + to_string(start) + " out of range.";
            return false;
        } else if (end >= vNum) {
            errMsg = "Error: vertex " + to_string(end) + " out of range.";
            return false;
        }
        data.push_back(start);
        data.push_back(end);
        return true;
    }
    return true;
}

void addEdges(vector<int> data, vector<vector<int>> &tempAdjList) {
    for (unsigned i = 0; i < data.size(); i += 2) {
        tempAdjList[data[i]].push_back(data[i + 1]);
        tempAdjList[data[i + 1]].push_back(data[i]);
    }
}

void BFS(vector<vector<int>> &adjList, vector<Vertex> &vertices, int start) {
    vertices[start].visit = 1;
    queue<int> q;
    q.push(start);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (unsigned i = 0; i < adjList[u].size(); i++) {
            if (vertices[adjList[u][i]].visit == 0) {
                vertices[adjList[u][i]].visit = 1;
                vertices[adjList[u][i]].prev = u;
                q.push(adjList[u][i]);
            }
        }
    }
}

bool Path(vector<Vertex> &vertices, int start, int end, vector<int> &path) {
    if (start == end) {
        path.push_back(start);
        return true;
    } else if (vertices[end].prev == -1) {
        cerr << "Error: Path does not exist!" << endl;
        return false;
    } else {
        Path(vertices, start, vertices[end].prev, path);
        path.push_back(end);
        return true;
    }
}

void showPath(vector<int> path) {
    for (unsigned i = 0; i < path.size() - 1; i++)
        cout << path[i] << "-";
    cout << path[path.size() - 1] << endl;
}

int main() {

    vector<Vertex> vertices;
    vector<vector<int>> adjList;
    CmdCheck check;

    while (!cin.eof()) {

        string line, errMsg;
        getline(cin, line);
        char cmd;
        vector<int> data;
        if (parseLine(line, cmd, check, vertices.size(), data, errMsg)) {
            if (cmd == 'V') {
                vector<Vertex> tempVertices(data[0]);
                vertices = tempVertices;
            } else if (cmd == 'E') {
                //modified for a3
                string vStdOut, eStdOut;
                vStdOut = "V " + to_string(vertices.size());
                size_t pos = line.find("{");
                eStdOut = "E " + line.substr(pos);
                //end modified for a3
                vector<vector<int>> tempAdjList(vertices.size());
                addEdges(data, tempAdjList);
                adjList = tempAdjList;
                //modified for a3
                cout << vStdOut << endl;
                cout << eStdOut << endl;
                //end modified for a3
            } else if (cmd == 's') {
                vector<Vertex> tempVertices = vertices;
                BFS(adjList, tempVertices, data[0]);
                vector<int> path;
                if (Path(tempVertices, data[0], data[1], path))
                    showPath(path);
            }
        } else {
            if (!errMsg.empty())
                cerr << errMsg << endl;
        }
    }
}
