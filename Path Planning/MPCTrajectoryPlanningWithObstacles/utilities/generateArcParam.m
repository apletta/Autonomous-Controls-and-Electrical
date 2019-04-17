function track = generateArcParam(track)
    track.s = [];
    
    for i = 1:track.len
        track.s(end+1) = arclength(track.x(1:i), track.y(1:i));
    end
    