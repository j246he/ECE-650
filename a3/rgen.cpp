#include <iostream>
#include <vector>
#include <fstream>
#include <unistd.h>

using namespace std;

struct Point {
    int x;
    int y;
};

bool checkStreet(vector<Point> sCoors, Point coor) {
    if (sCoors.empty())
        return true;

    if (sCoors.size() == 1) {
        if (coor.x == sCoors[0].x && coor.y == sCoors[0].y)
            return false;
        else
            return true;
    }

    float x1, y1, x2, y2;
    x1 = sCoors[sCoors.size() - 1].x;
    y1 = sCoors[sCoors.size() - 1].y;
    x2 = coor.x;
    y2 = coor.y;

    for (unsigned i = 0; i < sCoors.size() - 1; ++i) {
        float x3, y3, x4, y4;
        x3 = sCoors[i].x;
        y3 = sCoors[i].y;
        x4 = sCoors[i + 1].x;
        y4 = sCoors[i + 1].y;

        float xnum = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4);
        float xden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
        float ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4);
        float yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);

        //with the last line-segment
        if (i == sCoors.size() - 2) {
            if (xnum == 0 && xden == 0 && ynum == 0 && yden == 0)
                return false;
            return true;
        }

        float xcoor = xnum / xden, ycoor = ynum / yden;

        float xminl1 = min(x1, x2), xmaxl1 = max(x1, x2);
        float yminl1 = min(y1, y2), ymaxl1 = max(y1, y2);
        float xminl2 = min(x3, x4), xmaxl2 = max(x3, x4);
        float yminl2 = min(y3, y4), ymaxl2 = max(y3, y4);

        if (((xcoor < xminl1 || xcoor > xmaxl1) || (ycoor < yminl1 || ycoor > ymaxl1)) ||
            ((xcoor < xminl2 || xcoor > xmaxl2) || (ycoor < yminl2 || ycoor > ymaxl2)))
            continue;
        return false;
    }
    return true;
}

int randomNumber(int min, int max) {
    ifstream urandom("/dev/urandom");

    if (urandom.fail())
        cerr << "Error: cannot open /dev/urandom" << endl;

    int num = 23; //a lucky number
    urandom.read((char *) &num, sizeof(int));
    urandom.close();

    return abs(num) % (max - min + 1) + min;
}

void genCmdR(vector<string> &streetName) {
    for (unsigned i = 0; i < streetName.size(); ++i)
        cout << "r \"" + streetName[i] + "\"" << endl;
    streetName.clear();
}

bool checkStreetName(vector<string> streetName, string sName) {
    for (unsigned i = 0; i < streetName.size(); ++i) {
        if (streetName[i] == sName)
            return false;
    }
    return true;
}

void genStreetName(vector<string> &streetName, int s) {
    int sNum = randomNumber(2, s);
    for (int i = 0; i < sNum;) {
        string sName;
        for (int j = 0; j < 3; j++) {
            char ch = (char) randomNumber(97, 122);
            sName += ch;
        }
        if (checkStreetName(streetName, sName)) {
            streetName.push_back(sName);
            ++i;
        }
    }
}

void genCmdA(vector<string> streetName, int n, int c, int &error) {
    for (unsigned i = 0; i < streetName.size(); ++i) {
        string cmdA = "a \"" + streetName[i] + "\" ";
        int nNum = randomNumber(1, n);
        vector<Point> sCoors;
        for (int j = 0; j < nNum + 1;) {
            Point coor;
            coor.x = randomNumber(-c, c);
            coor.y = randomNumber(-c, c);
            if (checkStreet(sCoors, coor)) {
                cmdA += "(" + to_string(coor.x) + "," + to_string(coor.y) + ")";
                sCoors.push_back(coor);
                ++j;
            } else {
                error++;
                if (error == 25) {
                    cerr << "Error: failed to generate valid input for 25 simultaneous attempts" << endl;
                    exit(1);
                }
            }
        }
        cout << cmdA << endl;
    }
}

int main(int argc, char **argv) {

    int cmd, s = 10, n = 5, l = 5, c = 20;
    int index;
    opterr = 0;
    while ((cmd = getopt(argc, argv, "s:n:l:c:")) != -1) {
        switch (cmd) {
            case 's':
                if (optarg) {
                    if (atoi(optarg) >= 2) {
                        s = atoi(optarg);
                    } else {
                        cerr << "Error: s should be larger than or equal to 2." << endl;
                        exit(1);
                    }
                }
                break;
            case 'n':
                if (optarg) {
                    if (atoi(optarg) >= 1) {
                        n = atoi(optarg);
                    } else {
                        cerr << "Error: n should be larger than or equal to 1." << endl;
                        exit(1);
                    }
                }
                break;
            case 'l':
                if (optarg) {
                    if (atoi(optarg) >= 5) {
                        l = atoi(optarg);
                    } else {
                        cerr << "Error: l should be larger than or equal to 5." << endl;
                        exit(1);
                    }
                }
                break;
            case 'c':
                if (optarg) {
                    if (atoi(optarg) >= 1) {
                        c = atoi(optarg);
                    } else {
                        cerr << "Error: c should be larger than or equal to 1." << endl;
                        exit(1);
                    }
                }
                break;
            case '?':
                if (optopt == 's' || optopt == 'n' || optopt == 'l' || optopt == 'c')
                    cerr << "Error: option -" << (char) optopt << " requires an argument." << endl;
                else
                    cerr << "Error: unknown option: " << (char) optopt << endl;
                exit(1);
            default:
                return 0;
        }
    }

    if (optind < argc) {
        cerr << "Found positional arguments" << endl;
        for (index = optind; index < argc; index++)
            cerr << "Non-option argument: " << argv[index] << endl;
        exit(1);
    }

    vector<string> streetName;
    while (true) {
        int error = 0;
        genCmdR(streetName);
        genStreetName(streetName, s);
        genCmdA(streetName, n, c, error);
        cout << "g" << endl;
        sleep(randomNumber(5, l));
    }

    return 0;
}
