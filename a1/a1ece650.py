import sys
from parseLine import *

def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        try:
           parseLine(line)
        except Exception as ex:
            print ex

if __name__ == '__main__':
    main()
