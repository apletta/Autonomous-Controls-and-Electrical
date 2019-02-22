% Loads data values from file path provided and creates a spline of the
% loaded points.
% Takes in the file path and the number of points the spline should
% interpolate.
% Returns the points in [x;y] format, x,y and the spline function
function cp = loadData(numOfPoints)

% Read csv
[points,widths,~] = getData('Data/TrackData.csv');
[x,y] = points2xy(points);

% Interpolate data and evaluate points at a fixed distance of separation
t = 0:(1/(numOfPoints)):1;
points = interparc(t,x,y,'csape')';
[x,y] = points2xy(points);

% Create checkpoints
cp = createCheckpoints(x,y,repmat(3,1,length(x)));
cg = createCheckpoints(x,y,repmat(2.5,1,length(x)));

% Plot points
if true
    [x,y,x1,y1,x2,y2] = points2xy(cp);
    [gx,gy,gx1,gy1,gx2,gy2] = points2xy(cg);
    plot([x;x1],[y;y1],'k',[x;x2],[y;y2],'k')
    fill([gx,gx1],[gy,gy1], ...
        'b','FaceAlpha',.2)
    fill([gx,gx2],[gy,gy2], ...
        'r','FaceAlpha',.2)
    plot(x,y,'k',x1,y1,'b',x2,y2,'r','LineWidth',2)
end

function [points,widths,length] = getData(filePath)
% Read data from csv
data = csvread(filePath)';

% Split data into track points and track widths
points = data(1:2,:);
widths = data(3,:);

% Close track loop by adding first point again
points = addInitialPoint(points);
widths = addInitialPoint(widths);

% Get length of the data
length = max(size(points));


function checkpoints = createCheckpoints(x,y,w)
tp = addInitialPoint([diff(x);diff(y)]);

% Tangent vectors to the centerline are computed
tp = w .* tp ./ vecnorm(tp);
[tx,ty] = points2xy(tp);

% Checkpoint matrix is created
checkpoints = [x; y;...
    x-ty;y+tx;
    x+ty;y-tx];
