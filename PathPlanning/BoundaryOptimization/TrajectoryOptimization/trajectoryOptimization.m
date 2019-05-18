% TODO: Cost function is based on a constant that needs to be specified
% TODO: Describe the path in terms of functions rather than discrete data
% TODO: Robust description of path through cones without quality spaced checkpoints
% TODO: Different optimziation technique?

% Trajectory Optimization Function
% Takes a track as a parameter
% Optimizes a nonlinear cost function that takes into account total
% distance along track and total curvature along the track to form a least
% curvature/distance optimization.

function traj = trajectoryOptimization(track)

% Gets boundary checkpoints
[x1,y1,x2,y2] = matrixTo1D(track.checkpoints);

len = length(y2);

% Sets up fmincon inputs
% Uses sqp nonlinear algorithm
x0 = repmat(0.01,1,len);
A = [];
B = [];
Aeq = [];
Beq = [];
LB = zeros(1,len);
UB = ones(1,len);
nonlcon = @nonlincon;
options = optimoptions('fmincon');
options.MaxFunctionEvaluations = 50000;
options.Algorithm = 'sqp';
options.Display = 'final';

tic
x = fmincon(@objective,x0,A,B,Aeq,Beq,LB,UB,nonlcon,options);
toc

% Creates the final trajectory to output from the optimized points
traj.x = x1 .* x + x2 .* (1 - x);
traj.y = y1 .* x + y2 .* (1 - x);

disp(['Inital Objective: ' num2str(objective(x0))])
disp(['Optimized Objective: ' num2str(objective(x))])

    function [c,ceq] = nonlincon(p)
        % Non-linear Constraints
        % Constrains the first and weights to be the same
        c = [];
        ceq = p(:,1) - p(:,end);
    end

    function cost = objective(p)
        % Objective function
        % Computes the distance and curvature of the path and returns a
        % cost based on the values.
        % Takes in a 1D array of weights that will be used to create a
        % trajectory path
        
        % End condition: sets the first and last as the same
        % p(1) = p(end);
        
        % Creates trajectory path as a weighted sum between the two 
        % boundaries.
        px = x1 .* p + x2 .* (1 - p);
        py = y1 .* p + y2 .* (1 - p);
        
        % Computes curvature and distance
        [k,ds] = distanceandcurvature(px,py);
        
        % Computes cost based on a weighted sum between the curvature and
        % the distance.
        c = .95;
        cost = c*sum(k) + (1-c)*sum(ds);
    end
end