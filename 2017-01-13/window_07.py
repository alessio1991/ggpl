from pyplasm import *



def getLength(list):
    length = 0
    for elem in list:
        length = length + elem
    return length

"""Input: X, Y, Z (corresponding to lateral quotes of type [float]), occupancy of type [bool]
   Output: hpc object"""
def window(X,Y,Z,occupancy):
    
    """Input: dx,dy,dz for box dimensioning, of type float,color of window and glass
       Output: hpc object"""
    def windowAux(dx,dy,dz,glassDepth,colorWindow,colorGlass):  
     
        length = getLength(X)
        window = []    
        
        for zI in range(0,len(Z)):
            vector = occupancy[zI]
            cont = 0
            
            for xI in vector:
                
                if xI==1:
                    window.append(colorWindow)
                    prodXY = PROD([QUOTE([X[cont]]),QUOTE(Y)])
                    prodXYZ = PROD([prodXY,QUOTE([Z[zI]])])
                    window.append(prodXYZ)   
                    
                if xI==0:
                    window.append(colorGlass)
                    prod1 = PROD([QUOTE([X[cont]]),QUOTE([glassDepth])])
                    prod2 = PROD([prod1,QUOTE([Z[zI]])])
                    window.append(T([1,2,3])([0,Y[0]/2-glassDepth/2,0]))
                    window.append(prod2)
                    window.append(T([1,2,3])([0,-Y[0]/2+glassDepth/2,0]))

                window.append(T([1,2,3])([X[cont],0,0]))
                cont = cont+1
                
            window.append(T([1,2,3])([-length,0,Z[zI]]))
            
        window.append(COLOR([139/255.,139/255.,139/255.]))
        window.append(T([1,2,3])([getLength(X)/2.,-.02,-getLength(Z)/2.]))
        handle = CUBOID([.02,.02,.1])
        window.append(handle)
        window=STRUCT(window)
        
        dim=[dx/SIZE(1)(window),dy/SIZE(2)(window),dz/SIZE(3)(window)]
        window= STRUCT([S([1,2,3])(dim),window])
        
        return window
    return windowAux