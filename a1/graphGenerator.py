from intersect import *

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
                        e.append((v.index(i[0]) + 1, v.index(i[1]) + 1))
                elif vTemp[j] == i[len(i) - 1]:
                    if i[len(i) - 2] not in v:
                        v.append(i[len(i) - 2])
                    if i[len(i) - 1] not in v:
                        v.append(i[len(i) - 1])
                    if (v.index(i[len(i) - 2]) + 1, v.index(i[len(i) - 1]) + 1) not in e:
                        e.append((v.index(i[len(i) - 2]) + 1, v.index(i[len(i) - 1]) + 1))
                else:
                    ind = i.index(vTemp[j])
                    if i[ind - 1] not in v:
                        v.append(i[ind - 1])
                    if i[ind] not in v:
                        v.append(i[ind])
                    if i[ind + 1] not in v:
                        v.append(i[ind + 1])
                    x, y, z = v.index(i[ind - 1]) + 1, v.index(i[ind]) + 1, v.index(i[ind + 1]) + 1
                    if (x, y) and (x, y) not in e:
                        e.append((x, y))
                    if (y, z) and (y, z) not in e:
                        e.append((y, z))
    #print V
    print 'V = {'
    for i in range(len(v)):
        print ' ' + str(i + 1) + ': (' + str(v[i][0]) + ',' + str(v[i][1]) + ')'  
    print '}'
    #print E
    print 'E = {'
    for i in range(len(e)):
        if i != len(e) - 1:
            print ' <' + str(e[i][0]) + ',' + str(e[i][1]) + '>,'
        else:
            print ' <' + str(e[i][0]) + ',' + str(e[i][1]) + '>'
    print '}'
