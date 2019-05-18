% Loads data values from file path provided and creates a spline of the
% loaded points.
% Takes in the file path and the number of points the spline should
% interpolate.
% Returns the points in [x;y] format, x,y and the spline function
function [blue,yellow,mids] = loadData(filePathNum,numOfPoints)

% Read csv
[bp,bl] = getData(sprintf('data/blue%s.csv',filePathNum));
[yp,yl] = getData(sprintf('data/yellow%s.csv',filePathNum));

% Repeats initial point to form a closed path
bp = addInitialPoint(bp);
yp = addInitialPoint(yp);

plot(bp(1,:), bp(2,:),'.r','MarkerSize',15)

% Creates a spline function
f = @(dataLength) (numOfPoints+1) / dataLength;
type = 'periodic';
blue.f = csape(1:bl+1,bp,type);
yellow.f = csape(1:yl+1,yp,type);
mids.f = fncmb(fncmb(yellow.f,.5),'+',fncmb(blue.f,.5));
%fnplt(mids.f)
%fnplt(blue.f)
%fnplt(yellow.f)

db = bl / numOfPoints;
bt = fnval(fnder(blue.f),1:db:bl+1);
[tx,ty] = matrixTo1D(bt);
blue.nx = -ty;
blue.ny = tx;


% Creates a discrete interpolation with a fixed distance between points
blue.p = interparc(linspace(0,1,numOfPoints),bp(1,:),bp(2,:),'csape')';
yellow.p = interparc(linspace(0,1,numOfPoints),yp(1,:),yp(2,:),'csape')';
%mids.p = interparc(linspace(0,1,numOfPoints),mp(1,:),mp(2,:),'linear')';

[blue.x,blue.y] = matrixTo1D(blue.p);
[yellow.x,yellow.y] = matrixTo1D(yellow.p);
%[mids.x,mids.y] = matrixTo1D(mids.p);

function [data,length] = getData(filePath)
data = csvread(filePath)';
length = max(size(data));
