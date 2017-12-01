import re
from graphGenerator import *

sName, sCoors = [],[]

def parseLine(line):
    tempLine = line.strip()

    if tempLine == 'g':
        return graphGenerator(sCoors)
    #cmd1 for r command, cmd2 for a or c command
    cmd1 = re.match(r'([r])\s+\"([a-zA-Z\s]*)\"', tempLine)
    cmd2 = re.match(r'([ac])\s+\"([a-zA-Z\s]*)\"\s+((\(\s*\-?\d+\s*,\s*\-?\d+\s*\)\s*)+)', tempLine)
    
    if cmd1 or cmd2:
        #remove a street
        if cmd1:
            if re.findall(r'\(\s*-?\d+\s*,\s*-?\d+\s*\)', tempLine):
                raise Exception('Error: r command should not have coordinates!')
            name = cmd1.group(2).lower()
            if name not in sName:
                raise Exception('Error: no such street in database!')
            else:
                sCoors.pop(sName.index(name))
                sName.pop(sName.index(name))
        #add or change a street
        elif cmd2:
            name = cmd2.group(2).lower()
            coors = re.findall(r'\(\s*-?\d+\s*,\s*-?\d+\s*\)', cmd2.group(3))
            for i in range(len(coors)):
                x = re.findall(r'-?\d+', coors[i])
                coors[i] = (int(x[0]), int(x[1]))
            #add a street
            if cmd2.group(1) == 'a':
                if name in sName:
                    raise Exception('Error: street already exists!')
                else:
                    sName.append(name)
                    sCoors.append(coors)
            #change a street
            elif cmd2.group(1) == 'c':
                if name not in sName:
                    raise Exception('Error: no such street in database!')
                else:
                    sCoors[sName.index(name)] = coors
    else:
        if tempLine == '':
            raise Exception('Error: please enter a valid string then press the Enter key...')
        elif tempLine[0] == 'g' and len(tempLine) != 1:
            raise Exception('Error: g command cannot have any characters after it')
        elif tempLine[0] not in ('a', 'c', 'r'):
            raise Exception('Error: command should start with a, c, r or g')
        elif not re.findall(r'\"([a-zA-Z\s]*)\"', tempLine):
            raise Exception('Error: street names can only be alphabetical and space')
        else:
            raise Exception('Error: input error, please re-enter...')
