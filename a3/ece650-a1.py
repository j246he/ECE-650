import sys
import re

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


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)

class Line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

def intersect(line1, line2):
    #if parallel to the x axis or y axis or each other
    x1, y1 = line1.src.x, line1.src.y
    x2, y2 = line1.dst.x, line1.dst.y
    x3, y3 = line2.src.x, line2.src.y
    x4, y4 = line2.dst.x, line2.dst.y

    xnum = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    xden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    #if xnum, ynum, xden, yden all equal to 0, which means two lines are overlapped or all coincident.
    if xnum == 0 and ynum == 0 and xden == 0 and yden == 0:
        if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2):
            return

        l = [x1, y1, x2, y2, x3, y3, x4, y4]
        for i in range(len(l)):
            l[i] = int(l[i]) if l[i] == round(l[i]) else round(l[i], 2)

        segment = [(l[0], l[1]), (l[2], l[3]), (l[4], l[5]), (l[6], l[7])]
        
        dic = {}
        for item in segment:
            if item not in dic:
                dic[item] = 1
            else:
                dic[item] += 1 

        if len(dic) == 2:
            return 
        elif len(dic) == 3:
            for item in dic:
                if dic[item] == 2:
                    return item
        elif len(dic) == 4:
            segment.sort()
            return segment[1],segment[2]

    #Two lines are parallel but there is no intersections
    if xden == 0 or yden == 0:    return
    xcoor, ycoor = xnum / xden, ynum / yden
    
    #bounded check
    xminl1, xmaxl1, yminl1, ymaxl1 = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
    xminl2, xmaxl2, yminl2, ymaxl2 = min(x3, x4), max(x3, x4), min(y3, y4), max(y3, y4)

    if ((xcoor < xminl1 or xcoor > xmaxl1) or (ycoor < yminl1 or ycoor > ymaxl1)) or ((xcoor < xminl2 or xcoor > xmaxl2) or (ycoor < yminl2 or ycoor > ymaxl2)):
        return 

    xcoor = int(xcoor) if xcoor == round(xcoor) else round(xcoor,2)
    ycoor = int(ycoor) if ycoor == round(ycoor) else round(ycoor,2)

    return (xcoor, ycoor)

def graphGenerator(sCoors):
    v, e, vTemp = [], [], []
    sTemp = [[sCoors[i][j] for j in range(len(sCoors[i]))] for i in range(len(sCoors))]

    for i in range(len(sCoors) - 1):
        for j in range(i + 1, len(sCoors)):
            for k in range(len(sCoors[i]) - 1):
                x1, y1 = sCoors[i][k][0],sCoors[i][k][1]
                x2, y2 = sCoors[i][k + 1][0], sCoors[i][k + 1][1]

                for l in range(len(sCoors[j]) - 1):
                    x3, y3 = sCoors[j][l][0], sCoors[j][l][1]
                    x4, y4 = sCoors[j][l + 1][0], sCoors[j][l + 1][1]
                    a, b, c, d = Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4)
                    l1, l2 = Line(a, b), Line(c, d)

                    if intersect(l1, l2):
                        if type(intersect(l1,l2)[0]) == tuple:
                            fst_int = intersect(l1,l2)[0]
                            sec_int = intersect(l1,l2)[1]
                            if fst_int not in vTemp:
                                vTemp.append(fst_int)
                            if fst_int not in sTemp[i]:
                                sTemp[i].insert(sTemp[i].index((x2, y2)), fst_int)
                            if fst_int not in sTemp[j]:
                                sTemp[j].insert(sTemp[j].index((x4, y4)), fst_int)
                            if sec_int not in vTemp:
                                vTemp.append(sec_int)
                            if sec_int not in sTemp[i]:
                                sTemp[i].insert(sTemp[i].index((x2, y2)), sec_int)
                            if sec_int not in sTemp[j]:
                                sTemp[j].insert(sTemp[j].index((x4, y4)), sec_int)
                        else:
                            (x, y) = intersect(l1, l2)
                            if (x, y) not in vTemp:
                                vTemp.append((x, y))
                            if (x, y) not in sTemp[i]:
                                sTemp[i].insert(sTemp[i].index((x2, y2)), (x, y))
                            if (x, y) not in sTemp[j]:
                                sTemp[j].insert(sTemp[j].index((x4, y4)), (x, y))
    
    #operate sTemp
    for i in range(len(sCoors)):
        for j in range(len(sCoors[i]) - 1):
            indS, indE = sTemp[i].index(sCoors[i][j]), sTemp[i].index(sCoors[i][j + 1])
            if indE - indS > 2:
                if sCoors[i][j][0] < sCoors[i][j + 1][0]:
                    sTemp[i][indS + 1:indE] = sorted(sTemp[i][indS + 1:indE])
                elif sCoors[i][j][0] > sCoors[i][j + 1][0]:
                    sTemp[i][indS + 1:indE] = sorted(sTemp[i][indS + 1:indE])[::-1]
                elif sCoors[i][j][1] < sCoors[i][j + 1][1]:
                    sTemp[i][indS + 1:indE] = sorted(sTemp[i][indS + 1:indE])
                elif sCoors[i][j][1] > sCoors[i][j + 1][1]:
                    sTemp[i][indS + 1:indE] = sorted(sTemp[i][indS + 1:indE])[::-1]

    #generate v and e
    for i in sTemp:
        for j in range(len(vTemp)):
            if vTemp[j] in i:
                if vTemp[j] == i[0]:
                    if i[0] not in v:
                        v.append(i[0])
                    if i[1] not in v:
                        v.append(i[1])
                    if (v.index(i[0]) + 1, v.index(i[1]) + 1) not in e:
                        e.append((v.index(i[0]), v.index(i[1])))
                elif vTemp[j] == i[len(i) - 1]:
                    if i[len(i) - 2] not in v:
                        v.append(i[len(i) - 2])
                    if i[len(i) - 1] not in v:
                        v.append(i[len(i) - 1])
                    if (v.index(i[len(i) - 2]) + 1, v.index(i[len(i) - 1]) + 1) not in e:
                        e.append((v.index(i[len(i) - 2]), v.index(i[len(i) - 1])))
                else:
                    ind = i.index(vTemp[j])
                    if i[ind - 1] not in v:
                        v.append(i[ind - 1])
                    if i[ind] not in v:
                        v.append(i[ind])
                    if i[ind + 1] not in v:
                        v.append(i[ind + 1])
                    x, y, z = v.index(i[ind - 1]), v.index(i[ind]), v.index(i[ind + 1])
                    if (x, y) and (x, y) not in e:
                        e.append((x, y))
                    if (y, z) and (y, z) not in e:
                        e.append((y, z))
  
    #print V
    print 'V ' + str(len(v))

    #print E
    sys.stdout.write('E {')
    for i in range(len(e)):
        if i != len(e) - 1:
            sys.stdout.write('<' + str(e[i][0]) + ',' + str(e[i][1]) + '>,')
        else:
            sys.stdout.write('<' + str(e[i][0]) + ',' + str(e[i][1]) + '>')
    print '}'
    sys.stdout.flush()

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
