function track = createBoundaries(track)
    tp = addInitialPoint([diff(track.x);diff(track.y)]);
    
    % Tangent vectors to the centerline are computed
    tp = (track.w/2) .* tp ./ vecnorm(tp);
    [tx,ty] = splitMatrix(tp);
    
    % Checkpoint matrix is created
    track.bx = track.x - ty; track.by = track.y + tx;
    track.yx = track.x + ty; track.yy = track.y - tx;
%     checkpoints = [x; y;...
%         x-ty;y+tx;
%         x+ty;y-tx];
end