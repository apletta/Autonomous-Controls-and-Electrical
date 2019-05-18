% Optimziation plotter
% Takes a string parameter that determines the type of plot that will be
% created. Also takes a track and trajectory parameter that is being
% plotted
function plotOptimization(track,trajectory,varargin)

hold on

for param = varargin
    % Draws obstacles
    if strcmp(param, 'obstacles')
        drawObstacles();
        
    % Draws checkpoints
    elseif strcmp(param, 'checkpoints')
        [x1,y1,x2,y2] = matrixTo1D(track.checkpoints);
        path.x = [x1;x2];
        path.y = [y1;y2];
        drawPath(path,'-b');
        
    % Draws track obstacle midpoints
    elseif strcmp(param, 'midPoints')
        drawPath(track.midPoints,'-r');
        
    % Draws trajectory
    elseif strcmp(param, 'trajectory')
        drawPath(trajectory,'-r');
        
    % Draws forward vectors of trajectory
    elseif strcmp(param, 'heading')
        drawVectors(trajectory,track.compute_vectors(trajectory.points));
        
    % Draws velocity gradient on the 2D plane
    elseif strcmp(param, 'velocity2D')
        drawGradient(trajectory,trajectory.v,param);
        
    % Draws velocity gradient on the 3D plane
    elseif strcmp(param, 'velocity3D')
        drawGradient(trajectory,trajectory.v,param);
        
    % Draws velocity vs distance
    elseif strcmp(param, 'velocityAnalysis')
        figure
        drawGraph(trajectory.ts,trajectory.v(1:end-1));
        
    % Draws curvature vs distance
    elseif strcmp(param, 'curvatureAnalysis')
        figure
        drawGraph(trajectory.ts,trajectory.k(1:end-1));
        
    % Throws error if param doesn't equal any of the previous
    else
        error('Invalid draw input');
    end
end

%% HELPER FUNCTIONS
    function drawObstacles()
        % Draws track boundary obstacles and the splines
        plot(track.blueX, track.blueY,'-k.', ...
            'LineWidth', 2, 'MarkerSize', 20);
        plot(track.yellowX, track.yellowY,'-k.', ...
            'LineWidth', 2, 'MarkerSize', 20);
    end

    function drawPath(path,color)
        % Draws specified path with the specified color
        plot(path.x, path.y, color, ...
            'LineWidth', 4, 'MarkerSize', 20,'MarkerEdgeColor',[1,1,0]);
    end

    function drawVectors(points,vectors)
        % Draws specified vectors at given points 
        quiver(points.x, points.y, vectors.x, vectors.y);
    end

    function drawGradient(path,v,param)
        % Draws gradient of specified path
        % Takes a parameter that determines which plane to plot on
        if strcmp(param, 'velocity2D')
            patch([path.x nan], [path.y nan], [v nan], ...
                'EdgeColor','interp','LineWidth',5)
        elseif strcmp(param, 'velocity3D')
            patch([path.x nan], [path.y nan], [v nan], [v nan], ...
                'EdgeColor','interp','LineWidth',5);
        end
    end

    function drawGraph(x,y)
        % Basic plot function
        plot(x,y);
    end
end