# parameters for calculating vehicle speed
ms2kmh = 3.6
vdlDistance = 20 # distance between VDLs
fps = 30 # input video's fps

def check_line(p1, p2, w):
    '''
    This is a function to check where the point w is based on a straight line.
    
    Args:
        p1: left point on a straight line
        p2: right point on a straight line
        w: point you want to know where you are in a straight line
    
    Returns: 
        x |- x > 0: w point is above a straight line
          |- x = 0: w point is on a straight line
          |- x < 0: w point is below a straight line
        
    '''
    x = (p2[0]-p1[0])*(w[1]-p1[1])-(w[0]-p1[0])*(p2[1]-p1[1])
    
    return x

def calcSpeed(track,luLine,ldLine,ruLine,rdLine,bbox,frame_idx):
    '''
    This is a function to calculate vehicle speed  when vehicles pass the two VDL line((luLine, ldLine) or (ruLine, rdLine))
    
    Args:
        track: Track class(Deep Sort reference code: https://github.com/nwojke/deep_sort/tree/master/deep_sort)
        * track.py has been updated to match our code
        luLine: left up line from an input frame
        ldLine: left down line from an input frame
        ruLine: right up line from an input frame
        rdLine: right down line from an input frame
        bbox: bounding box(bbox) obtain from Deep Sort. bbox format is (min x, min y, max x, max y). 
        frame_idx: frame number of an input video
    
    Returns: 
        track
    '''
    
    # We use bottom center point to calculate vehicle speed
    bottom_center = (int(((bbox[0])+(bbox[2]))/2),int(bbox[3])) 

    # When vehicle is on the 1,2,3 lanes, use luLane, ldLane to calculate vehicle speed
    if track.driving_lane == 1 or track.driving_lane == 2 or track.driving_lane == 3: # down lane
        # Save the time when up line pass
        if track.speed_update and check_line(luLine[0], luLine[1], bottom_center) < 0:
            track.time_passing_vline_start = frame_idx
        # Save the time when down line pass
        if track.speed_update and check_line(ldLine[0], ldLine[1], bottom_center) > 0:
            track.time_passing_vline_end = frame_idx
    # When vehicle is on the 4,5,6 lanes, use luLane, ldLane to calculate vehicle speed
    elif track.driving_lane == 4 or track.driving_lane == 5 or track.driving_lane == 6: # up lane
        # Save the time when down line pass
        if track.speed_update and check_line(rdLine[0], rdLine[1], bottom_center) > 0:
            track.time_passing_vline_start = frame_idx
        # Save the time when up line pass
        if track.speed_update and check_line(ruLine[0], ruLine[1], bottom_center) < 0:
            track.time_passing_vline_end = frame_idx 

    # Calculate the time that passed the two lines: time_passing_vline_end - time_passing_vline_start        
    if track.time_passing_vline_end > 0 and track.time_passing_vline_start > 0:
        track.speed_time = (track.time_passing_vline_end-track.time_passing_vline_start) * 1/fps
        if track.speed_update and track.speed_time > 0:
            track.speed_update = False

        if track.driving_lane == 1 or track.driving_lane == 2 or track.driving_lane == 3: # down lane
            if check_line(ldLine[1], ldLine[0], bottom_center) < 0:
                # Calculate the speed
                track.speed = vdlDistance/(track.speed_time)*ms2kmh
        else: # up lane
            if check_line(ruLine[1], ruLine[0], bottom_center) > 0:
                # Calculate the speed
                track.speed = vdlDistance/(track.speed_time)*ms2kmh
    
    return track
