% Loads data values from file path provided and creates a spline of the
% loaded points.
% Takes in the file path and the number of points the spline should
% interpolate.
% Returns the points in [x;y] format, x,y and the spline function
function [points,x,y,splineFunction] = loadData(filePath,numberOfPoints)

% Read csv
data = csvread(filePath)';
dataLength = length(data);

if false
    [x,y] = matrixTo1D(data);
    %plot(x,y,'.r','MarkerSize',40)
end

% Repeats initial point to form a closed path
data = addInitialPoint(data);

% Change in separation along the spline function
dp = (dataLength) / numberOfPoints;

% Creates a spline function
splineFunction = csape(1:dataLength+1,data,'periodic');

% Evaluates spline function along certain range of indicies
points = ppval(splineFunction,1:dp:dataLength+1);

% Gets x and y values
[x,y] = matrixTo1D(points);
