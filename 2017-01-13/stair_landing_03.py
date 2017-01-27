from pyplasm import *
from larlib import *

"""input: dx,dy,dz,path of the texture of the stairs-landing
   output: Hpc Object - Stairs and landing"""

#2alzata+pedata=64cm ideal formule of stair's size
def ggpl_stair_landing(dx,dy,dz,texture):
    
    #variables
    alzata = .2
    gradini = dz/alzata    
    resto = modf(gradini)[0]    
    totGradiniIntero = modf(gradini)[1]
    newAlzata = dz/totGradiniIntero
    pedata =.64-(2*newAlzata)
    yLanding = dy/5.0
    pedataFraz = (dy-yLanding)
    newPedata = pedataFraz/(totGradiniIntero)
    larghezzaStair = dx/2.0
    
    #construct landing as a cuboid with the size calculate before
    landing = CUBOID([larghezzaStair*2,yLanding,newAlzata])
    
    #define the diagonale for fill the stairs
    diagonal=[]
    dist=[-(dx/2),dx/2]
    distDiagonal=QUOTE(dist)
    diagonal.append([0,newPedata])
    diagonal.append([newAlzata,newPedata])
    diagonal.append([newAlzata,2*newPedata])
    d=MKPOL([diagonal,[[1,2,3]],None])
    d=PROD([distDiagonal,d])
    d=STRUCT([R([2,3])(PI/2),d])
    d=STRUCT([R([1,2])(PI),d])
    d=STRUCT([T([1])(dx*3/2),d])
    
    #contruct first stair landing
    #i create every each single stair until the total stairs's number. 
    #stair is create as a cuboid with the size calculate before
    stairsLanding=[]
    for i in range (1,int(totGradiniIntero/2)):
        stairsLanding.append(CUBOID([larghezzaStair,newPedata,newAlzata]))
        stairsLanding.append(T([2,3])([newPedata,newAlzata]))
        d=STRUCT([d,T([2,3])([newPedata,newAlzata]),d])
    stairsLanding.append(landing)    
    d=STRUCT([T([1,2,3])([-dx/2,newAlzata-2*newPedata,-newAlzata]),d])
    
    #transform diagonal, ramp and their union in a STRUCT
    structD=STRUCT([d])
    structSL=STRUCT(stairsLanding)
    totalRamp=STRUCT([structD,structSL])
    
    #rotate and traslate the second ramp for create the second effective ramp
    ramp2Rotation=STRUCT([R([1,2])(PI),totalRamp])
    totalRamp2 = STRUCT([T([1,2,3])([dx,(newPedata*((totGradiniIntero)/2)-newPedata),(newAlzata*((totGradiniIntero)/2))]),ramp2Rotation])
    
    #assemble the two ramps before the return
    finalTotalRamps=STRUCT([totalRamp,totalRamp2])
    
    ramps = STRUCT([TEXTURE([texture+"/stairs.jpg", TRUE, FALSE, 1, 1, 0, 30, 30])(finalTotalRamps)])
    
    return ramps