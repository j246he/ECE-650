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
