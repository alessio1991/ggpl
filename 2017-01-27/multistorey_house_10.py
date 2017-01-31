from house_modeling_08 import *
from stair_landing_03 import *
from roof_09 import *
from window_07 import *
from door_07 import *

"""input:number of house (necessary for create more house) 
         and array with dimensions of house 
         (the dimensions wil be moltiplicated for 10mt on x, 20mt on y, and for 8 on z)
   output:hpc object representative the house"""
def ggpl_multistorey_house(numberHouse,dimHouse):
    
    """input:path of the .lines files
       output:hpc object representative the house"""
    def ggpl_multistorey_house_path(pathLinesFirstFloor,pathLinesSecondFloor):
        
        """input:5 array representative a set of color for the various house's elements
           output:hpc object representative the house"""
        def ggpl_multistorey_house_color(colorWalls,colorDoor,colorGlassDoor,colorWindow,colorGlassWindow):
        
            #create house's floors opportunely traslating
            first_floor = ggpl_house_modeling(pathLinesFirstFloor,colorWalls[numberHouse],
                                              "texture/house_"+str(numberHouse))
            height_first_floor = SIZE(3)(first_floor)

            #create and traslate the ramps
            ramps = ggpl_stair_landing(2.3, 5, 4, "texture/house_"+str(numberHouse))
            ramps = STRUCT([T([1,2])([.5,7.35]),ramps])

            #create windows (small and big) traslate and rotate
            XWindows=[.025,.1,.01,.1,.01,.1,.05,.1,.01,.1,.01,.1,.025]
            YWindows=[.3]
            ZWindows=[.025,.15,.01,.15,.05,.15,.01,.15,.01,.15,.025]
            occupancyWindows=[[1,1,1,1,1,1,1,1,1,1,1,1,1],
                              [1,0,1,0,1,0,1,0,1,0,1,0,1],
                              [1,1,1,1,1,1,1,1,1,1,1,1,1],
                              [1,0,1,0,1,0,1,0,1,0,1,0,1],
                              [1,1,1,1,1,1,1,1,1,1,1,1,1],
                              [1,0,1,0,1,0,1,0,1,0,1,0,1],
                              [1,1,1,1,1,1,1,1,1,1,1,1,1],
                              [1,0,1,0,1,0,1,0,1,0,1,0,1],
                              [1,1,1,1,1,1,1,1,1,1,1,1,1],
                              [1,0,1,0,1,0,1,0,1,0,1,0,1],
                              [1,1,1,1,1,1,1,1,1,1,1,1,1]]
            glassDepthWindows = .07
            windowSmall = window(XWindows,YWindows,ZWindows,occupancyWindows)(1.05,.15,1.04,glassDepthWindows,
                                                                             colorWindow[numberHouse],
                                                                             colorGlassWindow[numberHouse])
            windowBig = window(XWindows,YWindows,ZWindows,occupancyWindows)(1.85,.15,1.04,glassDepthWindows,
                                                                            colorWindow[numberHouse],
                                                                            colorGlassWindow[numberHouse])
            windowRotateFrontSmall = STRUCT([R([1,2])(PI),windowSmall])
            windowRotateFrontBig = STRUCT([R([1,2])(PI),windowBig])
            windowRotateDxSmall = STRUCT([R([1,2])(-PI/2),windowSmall])
            windowRotateDxBig = STRUCT([R([1,2])(-PI/2),windowBig])
            windowRotateSxSmall = STRUCT([R([1,2])(PI/2),windowSmall])
            windowRotateSxBig = STRUCT([R([1,2])(PI/2),windowBig])
            window1 = STRUCT([T([1,2,3])([1.88,6.25,1.2]),windowRotateFrontSmall])
            window2 = STRUCT([T([1,2,3])([8,.6,1.2]),windowRotateFrontSmall])
            window3 = STRUCT([T([1,2,3])([7.15,19.8,1.2]),windowBig])
            window4 = STRUCT([T([1,2,3])([10.2,5.4,1.2]),windowRotateDxSmall])
            window5 = STRUCT([T([1,2,3])([10.2,9.92,1.2]),windowRotateDxSmall])
            window6 = STRUCT([T([1,2,3])([10.2,13.815,1.2]),windowRotateDxSmall])
            window7 = STRUCT([T([1,2,3])([2.14,19.8,1.2]),windowSmall])
            window8 = STRUCT([T([1,2,3])([.45,12.76,1.2]),windowRotateSxSmall])
            window9 = STRUCT([T([1,2,3])([.45,17.13,1.2]),windowRotateSxBig])
            window10 = STRUCT([T([1,2,3])([4.75,4.35,1.2]),windowRotateSxSmall])

            #create door entrance traslate
            XDoor=[.2,.05,.15,.2,.5,.3,.1]
            YDoor=[.1]
            ZDoor=[.1,.2,.1,.2,.1,.2,.1,.2,.1,.2,.1,.2,.1,.2,.1]
            occupancyDoor=[[1,1,1,1,1,1,1],
                           [1,1,1,1,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,0,1,0,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,0,1,0,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,0,1,0,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,0,1,0,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,0,1,0,1,0,1],
                           [1,0,1,1,1,0,1],
                           [1,1,1,1,1,0,1],
                           [1,1,1,1,1,1,1]]

            glassDepthDoors = .03
            doorExt = door(XDoor,YDoor,ZDoor,occupancyDoor)(1.55,.15,2.25,glassDepthDoors,
                                                            colorDoor[numberHouse],
                                                            colorGlassDoor[numberHouse])
            doorExt = STRUCT([T([1,2,3])([3,6.05,.015]),doorExt])

            #create doors internal opportunely rotate and traslate
            XDoorInt=[.4,.5,.4]
            YDoorInt=[.05]
            ZDoorInt=[1,1,.25]
            occupancyDoorInt=[[1,1,1],
                              [1,0,1],
                              [1,1,1]]
            colorDoorInt = COLOR([139/255.,69/255.,19/255.])
            colorGlassInt = COLOR([103/255.,230/255.,236/255.])
            doorInt = door(XDoorInt,YDoorInt,ZDoorInt,occupancyDoorInt)(1.3,.05,2.25,
                                                                        glassDepthDoors,colorDoorInt,
                                                                        colorGlassInt)
            doorIntRotate = STRUCT([R([1,2])(PI/2),doorInt])
            doorInt1 = STRUCT([T([1,2,3])([8.15,10.1,.015]),doorInt])
            doorInt2 = STRUCT([T([1,2,3])([2.9,7.6,.015]),doorIntRotate])
            doorInt3 = STRUCT([T([1,2,3])([4.6,6.85,.015]),doorIntRotate])
            doorInt4 = STRUCT([T([1,2,3])([4.6,8.65,.015]),doorIntRotate])
            doorInt5 = STRUCT([T([1,2,3])([5.4,14.04,.015]),doorIntRotate])

            #define ceiling opportunely traslated
            ceiling = lines2lines("lines/second_floor/floor.lines")
            plan = STRUCT(AA(POLYLINE)(ceiling))
            plan = OFFSET([.015,.015])(plan)
            heigth = QUOTE([.009])
            plan3dFloor = PROD([plan,heigth])
            dim = [20,20,16]
            ceiling = STRUCT([S([1,2,3])(dim),plan3dFloor])
            ceiling = STRUCT([(colorWalls[numberHouse])(T([3])(3.85)(ceiling))])

            #define struct of first floor
            first_floor = STRUCT([first_floor,
                                  doorExt,doorInt1,doorInt2,doorInt3,doorInt4,doorInt5,
                                  window1,window2,window3,window4,window5,window6,window7,window8,window9,window10,
                                  ramps])


            #define second floor's elements
            second_floor = ggpl_house_modeling(pathLinesSecondFloor,colorWalls[numberHouse],
                                               "texture/house_"+str(numberHouse))
            second_floor = STRUCT([T([3])(height_first_floor),second_floor])

            #create windows of second floor
            window1 = STRUCT([T([1,2,3])([1.88,6.25,5.2]),windowRotateFrontSmall])
            window2 = STRUCT([T([1,2,3])([8.8,.6,5.2]),windowRotateFrontBig])
            window3 = STRUCT([T([1,2,3])([7.15,19.8,5.2]),windowSmall])
            window4 = STRUCT([T([1,2,3])([10.2,9.92,5.2]),windowRotateDxSmall])
            window5 = STRUCT([T([1,2,3])([10.2,13.815,5.2]),windowRotateDxSmall])
            window6 = STRUCT([T([1,2,3])([10.2,18.95,5.2]),windowRotateDxBig])
            window7 = STRUCT([T([1,2,3])([2.14,19.8,5.2]),windowBig])
            window8 = STRUCT([T([1,2,3])([.45,10.93,5.2]),windowRotateSxSmall])

            #create the doors of second floor
            doorInt1 = STRUCT([T([1,2,3])([8.9,7.6,4.015]),doorInt])
            doorInt2 = STRUCT([T([1,2,3])([2,12.85,4.015]),doorInt])
            doorInt3 = STRUCT([T([1,2,3])([4.8,10.25,4.015]),doorInt])
            doorInt4 = STRUCT([T([1,2,3])([6.15,10.45,4.015]),doorIntRotate])
            doorInt5 = STRUCT([T([1,2,3])([6.15,12.35,4.015]),doorIntRotate])
            doorInt6 = STRUCT([T([1,2,3])([4.85,14.2,4.015]),doorInt])
            doorInt7 = STRUCT([T([1,2,3])([2.8,6.1,4.015]),doorIntRotate])

            #create roof opportunely traslated, rotated and scaled
            colorRoof = "texture/house_"+str(numberHouse)
            colorTerrace = colorWalls[numberHouse]
            roof = ggpl_roof_terrace(pathLinesSecondFloor+"/roof.lines",5.4,100,colorRoof,colorTerrace)
            roof = STRUCT([R([2,3])(PI),roof])
            dim = [.0235,.0235,.0235]
            roof = STRUCT([S([1,2,3])(dim),roof])
            terrace = STRUCT([CUBOID([9.38,12.87,.3]),(T([1,2])([4.05,-5.25]))(CUBOID([5.33,5.25,.3]))])
            terrace = T([1,2,3])([.02,6.57,9.48])(terrace)
            terrace = TEXTURE(["texture/house_"+str(numberHouse)+"/terrace.jpg", TRUE, FALSE, 1, 1, 0, 3, 3])(terrace)
            roof = STRUCT([T([1,2,3])([-.7,20.2,9.8])(roof),terrace])

            #define struct of second floor
            second_floor = STRUCT([second_floor,
                                   window1,window2,window3,window4,window5,window6,window7,window8,
                                   doorInt1,doorInt2,doorInt3,doorInt4,doorInt5,doorInt6,doorInt7])

            #define all struct of the multistorey house
            multistorey_house = STRUCT([first_floor,ceiling,second_floor,roof])
            
            #scale house with input array
            multistorey_house = STRUCT([S([1,2,3])(dimHouse),multistorey_house])
            
            return multistorey_house
        
        return ggpl_multistorey_house_color
    
    return ggpl_multistorey_house_path