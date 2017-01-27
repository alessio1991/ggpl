from pyplasm import *
from scipy import *  
from numpy import *  
import math
import csv

"""input: lists of the coordinates xyz of the two vertex (vertex1,vertex2),
   the inclination angle of the flaps (angle),
   flap's length (length)
   direction's quadrant of the flap (direction)
   output: all the flap's vertexes"""
def vertexFlap(vertex1, vertex2, angle, length, direction):

    #order x & y
    if vertex1[1]>vertex2[1]:
        x=vertex1[0]
        y=vertex2[1]
    else:
        x=vertex2[0]
        y=vertex1[1]

    vertex3 = [x,y,0]

    #AB = sqrt[(x2- x1)^2 + (y2- y1)^2]
    distance12 = sqrt((vertex1[0]-vertex2[0])*(vertex1[0]-vertex2[0])
                      +(vertex1[1]-vertex2[1])*(vertex1[1]-vertex2[1]))
    distance13 = sqrt((vertex1[0]-vertex3[0])*(vertex1[0]-vertex3[0])
                      +(vertex1[1]-vertex3[1])*(vertex1[1]-vertex3[1]))
    distance23 = sqrt((vertex2[0]-vertex3[0])*(vertex2[0]-vertex3[0])
                      +(vertex2[1]-vertex3[1])*(vertex2[1]-vertex3[1]))
    
    #distance23 = distance12 * cos(a)
    #cos(a) = distance23/distance12
    a = math.asin(distance23/distance12)
    b = PI/2-a

    distance24 = length * math.cos(angle)

    h = sqrt(length*length-distance24*distance24)
    distance25 = distance24 * math.cos(b)
    distance45 = sqrt(distance24*distance24-distance25*distance25)

    #verify the quadrant's number
    if direction==1:
        vertex6 = [vertex2[0]+distance25,vertex2[1]+distance45,h]
        vertex7 = [vertex1[0]+distance25,vertex1[1]+distance45,h]
    elif direction==2:
        vertex6 = [vertex2[0]-distance25,vertex2[1]+distance45,h]
        vertex7 = [vertex1[0]-distance25,vertex1[1]+distance45,h]
    elif direction==3:
        vertex6 = [vertex2[0]-distance25,vertex2[1]-distance45,h]
        vertex7 = [vertex1[0]-distance25,vertex1[1]-distance45,h]
    elif direction==4:
        vertex6 = [vertex2[0]+distance25,vertex2[1]-distance45,h]
        vertex7 = [vertex1[0]+distance25,vertex1[1]-distance45,h]

    #add all vertex find
    allVertexes = [vertex1,vertex2,vertex6,vertex7]

    return allVertexes

"""input: 2 lists of coordinates xy of the 2 vertexes/points
   output: a line as list of 3 elements (x,y,n, where n is the sum of x,y)"""
def points2line(vertex1,vertex2):

    x1=vertex1[0]
    x2=vertex2[0]
    y1=vertex1[1]
    y2=vertex2[1]
    m=0
    q=0

    if x1==x2:            #if the vertexes have same x, the line is parallel to y axis
        line = [1,0,x1]
    elif y1==y2:          #if the vertexes have same y, the line is parallel to x axis
        line = [0,1,y1]
    else:
        m=(float(y2)-float(y1))/(float(x2)-float(x1))
        q=float(y1)-m*float(x1)
        line = [-m,1,q]

    return line

"""input: 2 lines
    output: intersection's point"""
def linesIntersection(line1,line2):
      
    #coefficients on the left of the equals
    A = matrix([[line1[0], line1[1]], [line2[0], line2[1]]])  
    
    #knowns terms 
    b = array([line1[2], line2[2]])  
      
    #resolve linear system
    intersectionPoint = linalg.solve(A, b)
    
    return intersectionPoint

"""input: list of vertexes of all plans belonging to all flaps
   output: list of the directions of all flaps"""
def getDirections(vertexes):
    
    directions=[]
    
    for i in range(1,len(vertexes)):
        x1=vertexes[i-1][0]
        x2=vertexes[i][0]
        y1=vertexes[i-1][1]
        y2=vertexes[i][1]
        
        #compare the vertexes to determinate the quadrant's number
        if x2>=x1:
            if y2>=y1:
                directions.append(4)
            else:
                directions.append(3)  
        else:
            if y2>=y1:
                directions.append(1)
            else:
                directions.append(2)
                
    return directions

"""input: .lines file
   output: list of all vertexes of the floor plan"""
def getVertexes(path):
    
    with open(path, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        
        #append points as couple of coordinates xy (01 & 23)
        temp=[]
        for row in reader:
            temp.append([float(row[0]),float(row[1])])
            temp.append([float(row[2]),float(row[3])])

        #take only vertexes with even index (because they are the exactly vertexes of the floor plan)
        vertexes=[]
        for i in range(len(temp)):
            if i%2==0:
                vertexes.append(temp[i])
            if i==len(temp)-3:
                vertexes.append(temp[i])
                
    return vertexes

"""input: path of .lines's file, angle of flaps's inclinations, flaps's length,path for the color of roof and terrace
   output: final structure of roof & terrace"""
def ggpl_roof_terrace(path,angle,length,colorRoof,colorTerrace):

    #define the vertexes of the floor plan, and the directions of all plan of alla flaps
    vertexes=getVertexes(path)
    directions=getDirections(vertexes)

    #opportunely direction of the flaps in relation to the adjacent flaps
    flaps = []
    for i in range(len(directions)):
        if i==len(directions)-1:
            flaps.append(vertexFlap(vertexes[i],vertexes[0],angle,length,directions[i]))
        else:
            s = i+1
            flaps.append(vertexFlap(vertexes[i],vertexes[s],angle,length,directions[i]))

    #define lines and their intersection's point, of all lines in the "roof"
    lines = []
    for i in range(len(flaps)):
        lines.append(points2line(flaps[i][2],flaps[i][3]))

    intersections = []
    for i in range(len(lines)):
        if i==len(lines)-1:
            intersections.append(linesIntersection(lines[i],lines[0]))
            intersections.append(linesIntersection(lines[i],lines[0]))
        else:
            s = i+1
            intersections.append(linesIntersection(lines[i],lines[s]))

    #make final flaps with opportune direction and texture
    finalFlaps = []
    for i in range(len(directions)):
        
        if i == 0:           
            f = MKPOL([[
                        [flaps[i][0][0],flaps[i][0][1],0],
                        [flaps[i][1][0],flaps[i][1][1],0],
                        [intersections[i][0],intersections[i][1],flaps[1][2][2]],
                        [intersections[len(directions)-1][0],intersections[len(directions)-1][1],flaps[0][2][2]]],
                       [[1,2,3,4]],None])
            
            f = TEXTURE([colorRoof+"/roof.jpg", TRUE, FALSE, 1, 1, 0, 4, 4])(f)            
            finalFlaps.append(f)
            
        else:
            f = MKPOL([[[flaps[i][0][0],flaps[i][0][1],0],
                        [flaps[i][1][0],flaps[i][1][1],0],
                        [intersections[i][0],intersections[i][1],flaps[1][2][2]],
                        [intersections[i-1][0],intersections[i-1][1],flaps[0][2][2]]],
                       [[1,2,3,4]],None])
            
            f = TEXTURE([colorRoof+"/roof.jpg", TRUE, FALSE, 1, 1, 0, 4, 4])(f) 
            finalFlaps.append(f)

    #define border vertexes for create the terrace as polyline+solidify
    borderVertexes = [[] for _ in range(len(intersections)+1)]
    cell = []
    for i in range (len(intersections)):
        borderVertexes[i].append(intersections[i][0])
        borderVertexes[i].append(intersections[i][1])
        s = i+1
        if i==len(intersections)-1:
            borderVertexes[s].append(intersections[0][0])
            borderVertexes[s].append(intersections[0][1])
        cell.append(s)

    border = POLYLINE(borderVertexes)
    border = SOLIDIFY(border)

    #opportunely shift and texture
    terrace = T(3)(flaps[0][2][2])(border)
    terrace = colorTerrace(terrace)
    
    #struct final roof and roof+terrace
    roof = STRUCT(finalFlaps)
    roofTerrace=STRUCT([terrace,roof])
    
    return roofTerrace