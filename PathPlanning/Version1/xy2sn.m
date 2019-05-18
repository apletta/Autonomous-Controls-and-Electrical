function [ s, n, l ] = xy2sn( x, y, centerlinex, centerliney, varargin )
%XY2SN: Transform cartesian to curvilinear orthogonal coordinates
%arguments:
%   x,y - jx1 real numeric vectors containing the x and y coordinates of the
%       points to be transformed
%   cx, cy - kx1 real numeric vectors containing the x and y coordinates of
%       the points describing the centerline
%   discretisation - integer specifying how many samples to use for
%       discretising the spline interpolation of the centerline.
%       Defaults to 10.
%       A value of 0 specifies the use of the full spline (very slow).
%
%output:
%   s - a jx1 real numeric vector containing the s-coordinates of the
%       transformed points, as fractional distances along the
%       centerline
%   n - a jx1 real numeric vector containing the n-coordinates of the
%       transformed points, as normal distances from the
%       centerline
%   l - the length of the centerline
%
%The function first calculates a spline passing through all points defining
%the centerline. For each point P to be transformed it then finds the closest
%point A on the spline, the distance s along the spline to A, and the
%signed normal distance n between the A and P.
%
%Requires the distance2curve and arclength functions by John D'Errico
%   http://www.mathworks.de/matlabcentral/fileexchange/34869-distance2curve
%   http://www.mathworks.com/matlabcentral/fileexchange/34871-arclength
%
%Based on Merwade et al (2005) "Geospatial Representation of River Channels"
%   Journal of Hydrological Engineering, 10, 243-251
%
%
%Usage example:
% % Generate test data
% dataX = sin( (0:0.01:1)' *2*pi) + (rand(101,1) - 0.5) * 0.4;
% dataY = (0:0.02:2)' - 0.4*sin((0:0.01:1)' *4*pi)  + ...
%     (rand(101,1)-0.5) * 0.4;
% 
% hold off
% scatter(dataX, dataY);
% 
% % Provide centerline path
% centerlineX = sin( (0:0.05:1)' *2*pi);
% centerlineX = [-0.2; centerlineX; 0.2];
% 
% centerlineY = (0:0.1:2)' - 0.4 * sin( (0:0.05:1)'*4*pi);
% centerlineY = [0.1; centerlineY; 1.9];
% 
% hold all
% plot(centerlineX, centerlineY);
% hold off
% 
% % Transform to flow-oriented S-N coordinate system
% [S, N, L] = xy2sn(dataX, dataY, centerlineX, centerlineY);
% 
% % Plot points in S-N coordinate system
% scatter(S*L, N, [], S, 'f')
% axis equal
% 
% % Plot points in X-Y coordinate system, using S for colour
% scatter(dataX, dataY, [], S, 'f')
% axis equal
% 
% 
% %% Generate a grid in the S-N coordinate system and transform it to X-Y
% gridlinesS=repmat( (0:0.02:1), 5, 1);
% gridlinesN=repmat( (-0.2:0.1:0.2)',1,51);
% plot(gridlinesS*L,gridlinesN, 'k')
% axis equal
% hold all
% plot(gridlinesS'*L,gridlinesN', 'k')
% hold off
% 
% [gridlinesX, gridlinesY] = sn2xy(gridlinesS, gridlinesN, ...
%     centerlineX, centerlineY);
% 
% % Reshape resulting vector back to matrix structure
% gridlinesX = reshape(gridlinesX, size(gridlinesS));
% gridlinesY = reshape(gridlinesY, size(gridlinesS));
% 
% % Plot data and grid in XY and SN coordinates
% subplot(3,2,[1 3])
% plot(gridlinesX,gridlinesY, 'k')
% axis equal
% hold all
% plot(gridlinesX',gridlinesY', 'k')
% colormap('winter')
% scatter(dataX, dataY, [], S, 'f')
% hold off
% subplot(3,2,[5:6])
% plot(gridlinesS*L,gridlinesN, 'k')
% hold all; axis equal; plot(gridlinesS'*L,gridlinesN', 'k')
% scatter(S*L, N, [], S, 'f')

if nargin == 4
    splinesampling = 10;
elseif nargin ==5
    splinesampling = varargin{1};
end
        
if splinesampling > 0
    % Use a linear approximation of the spline interpolation
    nCenterline = length(centerlinex);
    t = 1:nCenterline;
    ts = 1:1/splinesampling:nCenterline;
    cx = spline(t,centerlinex,ts)';
    cy = spline(t,centerliney,ts)';

    % Calculate length of centerline
    l = arclength(cx,cy,'linear');
else
    % Use the full spline interpolation
    l = arclength(centerlinex, centerliney, 'sp');
end


try
    if splinesampling > 0
        [P, n, s] = distance2curve([cx cy], [x y], 'linear');
    else
        [P, n, s] = distance2curve([centerlinex centerliney], [x y], 'sp');
    end
catch err
    if (strcmp(err.identifier,'MATLAB:unassignedOutputs'))
        error('MATLAB:xy2sn:distance2curveunpatched', ['There is a bug in the distance2curve function.\n'...
            'Please open the function file using "edit distance2curve.m"\n'...
            'and edit line 453 to read\n  if nargout == 3\ninstead of\n  if nargout > 3']);
    end
end

PX = P(:,1);
PY = P(:,2);

% Calculate tangential vectors on thalweg curve
if splinesampling > 0
    [~, Ct] = interparc(s, cx, cy, 'linear');
else
    [~, Ct] = interparc(s, centerlinex, centerliney, 'sp');
end

% Calculate normal vectors on thalweg curve
Cn = [Ct(:,2), -Ct(:,1)];

% Calculate angles between points and normal points
angleMP = atan2(PY-y, PX-x);

% Calculate angles of normal vectors
angleTn = atan2(Cn(:,2), Cn(:,1));

% Calculate signs
Nsign = (2 * ( abs(angleTn-angleMP) < (pi/2) ) ) - 1;

n = n.*Nsign;

% Convert normalized s to distance units
s = s * l;
end

