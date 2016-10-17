from larlib import *
  
def spaceFrame (beamSection, pillarSection, interPillarAxis, interPlaneHeights, priorityToBeamsOrPillars):
    """Build and return a space frame
    
    `interPillarAxis` --- The pattern of the distances between the axis of the pillars, used along the x and y direction
    `priorityToBeamsOrPillars` --- 1 for pillars, 0 for beams"""
    
    bx,bz=beamSection
    px,py=pillarSection
    beamPillarGap=bx-px
    """Possible gap between beam and pillar size"""
    fx=px*3
    fy=py*3
    fz=px*2
    """Size of foundations"""
    foundationPillarGap=fx-px
    """Gap between foundation and pillar size"""
    
    pillarX=[]
    """Intervals on the x,y axis, for pillars extrusion by cartesian product; contemplate size and position of pillars"""
    for distance in interPillarAxis:
        pillarX += [px,-(distance-px)]
    pillarX.append(px)

    beamX1=[]
    """Intervals on the x,y axis,for beams extrusion; contemplate size and position of beams"""
    for distance in interPillarAxis:
        beamX1 += [bx,-(distance-bx)]
    beamX1.append(bx)
    
    beamZ=[]
    """Intervals on the z axis, for beams extrusion; contemplate size and position of beams"""
    for distance in interPlaneHeights:
        beamZ += [-(distance-bz),bz]
    
    if priorityToBeamsOrPillars==1:
        """Priority to pillars"""
        
        pillars= PROD([PROD([QUOTE(pillarX),QUOTE(pillarX)]),QUOTE(interPlaneHeights)])
        """Pillars extrusion: pillars aren t suspended by beams, so all segments produced by QUOTE in the z direction 
        are full"""
        
        beamX2=[-interval for interval in pillarX]
        """Intervals on the x,y axis,for beams extrusion; contemplate size and position of beams.
        Giving priority to pillars, collocate beams just -among- pillars
        Then the sequence of full and void segments (in the next application of QUOTE), is ugual and opposite to
        the one of pillars"""
        
        beamXy=STRUCT([PROD([T(1)(-beamPillarGap/2)(QUOTE(beamX1)),QUOTE(beamX2)]),
                       PROD([QUOTE(beamX2),T(1)(-beamPillarGap/2)(QUOTE(beamX1))])]) 
        """Extrusion of beams on the xy plane; contemplate the gap between the sizes of pillars and beams, centrating 
        beams in respect to pillars"""  
        
    else:
        """Priority to beams"""
        
        pillars=PROD([PROD([QUOTE(pillarX),QUOTE(pillarX)]),QUOTE([-distance for distance in beamZ])])
        
        beamX2=[]
        for distance in interPillarAxis:
            beamX2 += [px,distance-px]
        beamX2.append(px)
        """Thanks to priority to beams, this time beams aren't confinated -among- pillars, but take up the whole line"""
        
        beamXy=STRUCT([PROD([T(1)(-beamPillarGap/2)(QUOTE(beamX1)),QUOTE(beamX2)]),
                       PROD([QUOTE(beamX2),T(1)(-beamPillarGap/2)(QUOTE(beamX1))])])
        """Extrusion of beams on the xy plane; contemplate the gap between the sizes of pillars and beams, centrating 
        beams in respect to pillars"""
        
    beams=PROD([beamXy,QUOTE(beamZ)])
    """Beams extrusion"""
    
    spaceFrameWithoutFoundations=STRUCT([pillars,(beams)])
    
    foundationX=[]
    """Intervals on the x,y axis, for fondations extrusion by cartesian product; contemplate size and position of 
    fondations"""
    for distance in interPillarAxis:
        foundationX += [fx,-(distance-fx)]
    foundationX.append(fx)
    
    foundations= PROD([PROD([QUOTE(foundationX),QUOTE(foundationX)]),QUOTE([fz])])
                   
    spaceFrame=STRUCT([T(3)(fz)(T([1,2])([foundationPillarGap/2,foundationPillarGap/2])(spaceFrameWithoutFoundations)),
                       foundations])
    """Generation of the complete space frame, relocating the one without foundations in the coordinate of foundations"""
    
    return spaceFrame

model=spaceFrame((40,25),(40,40),[800,900,800],[300,300,300,300],1)

VIEW(model)