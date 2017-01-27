from pyplasm import *

def getLength(list):
    length = 0
    for elem in list:
        length = length + elem
    return length

"""Input: X, Y, Z (corresponding to lateral quotes of type [float]), occupancy of type [bool]
   Output: hpc object"""
def door(X,Y,Z,occupancy):
    
    """Input: dx,dy,dz for box dimensioning, of type float,color of door and glass
       Output: hpc object"""
    def doorAux(dx,dy,dz,glassDepth,colorDoor,colorGlass):           
                  
        length = getLength(X)
        door = []        
        
        for zI in range(0,len(Z)):
            
            vector = occupancy[zI]
            cont = 0
            
            #slide boolean array
            for xI in vector:
                
                #if boolean is true, generate the door's frame
                #in the list i append color and the cartesian product of the lateral quotes
                if xI==1:
                    door.append(colorDoor)
                    prodXY = PROD([QUOTE([X[cont]]),QUOTE(Y)])
                    prodXYZ = PROD([prodXY,QUOTE([Z[zI]])])
                    door.append(prodXYZ)
                    
                #if boolean is false, generate the screen
                if xI==0:
                    door.append(colorGlass)
                    prod1 = PROD([QUOTE([X[cont]]),QUOTE([glassDepth])])
                    prod2 = PROD([prod1,QUOTE([Z[zI]])])
                    door.append(T([1,2,3])([0,Y[0]/2-glassDepth/2,0]))
                    door.append(prod2)
                    door.append(T([1,2,3])([0,-Y[0]/2+glassDepth/2,0])) 
                    
                door.append(T([1,2,3])([X[cont],0,0]))
                cont = cont+1                
            
            door.append(T([1,2,3])([-length,0,Z[zI]]))
        
        #define door's handle, opportunely colorated and traslate
        door.append(COLOR([224/255.,224/255.,224/255.,1]))
        door.append(T([1,2,3])([.03,-.01,-getLength(Z)/2]))
        handle = CUBOID([.05,.05,.05])
        door.append(handle)
        
        #generate the STRUCT of door starting by list complete before
        door=STRUCT(door)
        
        #scale the door
        dim=[dx/SIZE(1)(door),dy/SIZE(2)(door),dz/SIZE(3)(door)]
        door= STRUCT([S([1,2,3])(dim),door])
        
        #return hpc object to used in the main function
        return door
    
    #return final hpc object to view
    return doorAux