function repulsive = generateRepulsiveField(track)
    %% Generate some points
    
    nrows = 50;
    ncols = 50;
    
    obstacle = false(nrows, ncols);
    
    [x, y] = meshgrid (1:ncols, 1:nrows);
    
    %% Generate some obstacle
    track.xy = round(track.xy);
    %obstacle(round(track.xy)) = true
    t = round([[track.yx;track.yy],[track.bx;track.by]]);
    x = t(1,:);
    y = t(2,:);
    
    for i = 1:length(x)
        obstacle(x(i),y(i)) = true;
    end
    
    %obstacle (x, y) = true;
    
%     t = ((x - 200).^2 + (y - 50).^2) < 50^2;
%     obstacle(t) = true;
%     
%     t = ((x - 400).^2 + (y - 300).^2) < 100^2;
%     obstacle(t) = true;
    
    %% Compute distance transform
    
    d = bwdist(obstacle);
    
    % Rescale and transform distances
    
    d2 = (d/100) + 1;
    
    d0 = 2;
    nu = 900;
    
    repulsive = nu*((1./d2 - 1/d0).^2);
    
    repulsive (d2 > d0) = 0;
    
    
%     %% Display repulsive potential
%     
%     figure;
%     m = mesh (repulsive);
%     m.FaceLighting = 'phong';
%     axis equal;
%     
%     title ('Repulsive Potential');