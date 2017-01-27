from pyplasm import * 
from larlib import *

"""function to create a simple model of house, with walls, doors, windows and floor
   input:path for the .lines files,rgb color for the house,path for the texture
   output:hpc object represent the structure of the house, with the space for doors and windows"""
def ggpl_house_modeling(path,colorHouse,texture):
    
    #define the array for every part of the house, by lines2lines function of larlib
    external1 = lines2lines(path+"/perimeter.lines")
    internal1 = lines2lines(path+"/internal.lines")
    doors1 = lines2lines(path+"/doors.lines")
    windows1 = lines2lines(path+"/windows.lines")
    border1 = lines2lines(path+"/border.lines")
    floor1 = lines2lines(path+"/floor.lines")
    
    #polyline, offset, quote and prod every part of the house
    planExt = STRUCT(AA(POLYLINE)(external1))
    planExt = OFFSET([.015,.015])(planExt)
    heigthExt = QUOTE([.25])
    plan3dExt = PROD([planExt,heigthExt])
    
    planInt = STRUCT(AA(POLYLINE)(internal1))
    planInt = OFFSET([.007,.007])(planInt)
    heigthInt = QUOTE([.25])
    plan3dInt = PROD([planInt,heigthInt])
    
    #struct external and internal walls
    intAndExt = (STRUCT([plan3dInt,plan3dExt]))
    
    #polyline, offset, quote and prod every part of the house
    planDoors = STRUCT(AA(POLYLINE)(doors1))
    planDoors = OFFSET([.015,.015])(planDoors)
    heigthDoors = QUOTE([.14])
    plan3dDoors = PROD([planDoors,heigthDoors])
    
    planWindows = STRUCT(AA(POLYLINE)(windows1))
    planWindows = OFFSET([.015,.015])(planWindows)
    heigthWindows = QUOTE([.065])
    plan3dWindows = PROD([planWindows,heigthWindows])
    
    planBorder = STRUCT(AA(POLYLINE)(border1))
    planBorder = OFFSET([.015,.015])(planBorder)
    heigthBorder = QUOTE([.25])
    plan3dBorder = PROD([planBorder,heigthBorder])
    
    plan = STRUCT(AA(POLYLINE)(floor1))
    plan = OFFSET([.015,.015])(plan)
    heigth = QUOTE([.0008])
    plan3dFloor = PROD([plan,heigth])
    
    #define the struct of door and windows (traslate) for the difference
    doorAndWindow = STRUCT([plan3dDoors,plan3dBorder,T([1,2,3])([0,0,.075])(plan3dWindows)])
    
    #difference between external and internal walls, and door and windows
    deleteDoorAndWindow = DIFFERENCE([intAndExt,doorAndWindow])
   
    #apply a texture for every room of the house
    houseWithTexture = STRUCT([(colorHouse)(deleteDoorAndWindow),
                               TEXTURE([texture+"/floor.jpg", TRUE, FALSE, 1, 1, 0, 10, 10])(plan3dFloor)])
    
    #scale all the model (House LxPxA: 20x20x4 mt), wall 30cm of P, doors are heighted about 2,2mt
    #windows are traslated about 120cm to floor, and are heighted about 110cm
    dimHouse = [20,20,16]
    model_house = STRUCT([S([1,2,3])(dimHouse),houseWithTexture])
    
    house = STRUCT([model_house])
    return house