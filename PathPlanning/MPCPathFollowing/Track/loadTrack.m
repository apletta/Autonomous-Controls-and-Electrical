function track = loadTrack(trackName,N,isClosed)
    
    load(trackName,'x','y','w');
    l = length(x);
    
    if iscolumn(x); x = x'; end
    if iscolumn(y); y = y'; end
    if exist('w') && iscolumn(w); w = w'; 
    elseif ~exist('w')
        width = 3
        w = linspace(width,width,l);
    end
    
    if isClosed
        x = addInitialPoint(x);
        y = addInitialPoint(y);
        w = addInitialPoint(w);
        l = l + 1;
        method = 'csape';
    else
        method = 'spline';
    end
    
    t = 0:(1/(N-1)):1;
    
    points = interparc(t,x,y,method)';
    
    % Interpolates widths to get new track boundaries
    k = zeros(1,l);
    p1 = [x;y];
    for i = 1:l; [~,k(i)] = min(sum(abs((p1(:,i) - points)))); end
    k(1) = 1;
    
    [~,idx] = unique(k,'stable');
    idx=setxor(idx,1:numel(k));
    if ~isempty(idx)
        k(idx) = k(idx) + randn(1);
    end
    
    t = 1:N;
    
    track.w = interp1(k,w,t);
    [track.x,track.y] = splitMatrix(points);
    track.xy = points;
    track.len = length(track.xy);
    track = createBoundaries(track);
    [track.s,track.r,track.k] = generateArcParam(track);
    %track.r