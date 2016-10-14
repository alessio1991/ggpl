from pyplasm import*
from larlib import *

def newStructure(beamSection, pillarSection, distancePillar, height):
    px=pillarSection[0]
    py=pillarSection[1]
    pz=height[0]
    bx=beamSection[0]
    bz=beamSection[1]
    xPillar=[]
    yPillar=[]
    zPillar=[]
    xBeam=[]
    zBeam=[]
    yBeam=[py]
    lenBeam=0

#creo pilastri
    for i in distancePillar:
        xPillar=xPillar+[px,-i]
        yPillar=[py]
        lenBeam=lenBeam+i+px
        
#creo travi
    for i in height:
       zPillar=zPillar+[i,-bz]
       zBeam=zBeam+[-i,bz]
    xBeam=[lenBeam+px]
    xPillar=xPillar+[px]   
    aPillar=PROD([QUOTE(yPillar),QUOTE(zPillar)])
    pillar=PROD([QUOTE(xPillar),aPillar])

    aBeam=PROD([QUOTE(yBeam),QUOTE(zBeam)])
    beam=PROD([QUOTE(xBeam),aBeam])
    VIEW(STRUCT([pillar, beam]))

newStructure((.4,.4),(.4,.4),[4,4,4],[3,3,3])