function track = loadTrack(trackName,N,isClosed)

load(trackName,'x','y','w');

if iscolumn(x); x = x'; end
if iscolumn(y); y = y'; end

if isClosed
    x = addInitialPoint(x);
    y = addInitialPoint(y);
    method = 'csape';
else
    method = 'spline';
end

t = 0:(1/(N-1)):1;

points = interparc(t,x,y,method)';

% Interpolates widths to get new track boundaries
l = length(x);
k = zeros(1,l);
p1 = [x;y];
for i = 1:l; [~,k(i)] = min(sum(abs((p1(:,i) - points)))); end
k(1) = 1;

[~,idx] = unique(k,'stable');
idx=setxor(idx,1:numel(k));
if ~isempty(idx)
    k(idx) = k(idx) + randn(1);
end

t = 1:length(points);
if ~exist('w')
    w = linspace(3,3,l);
end

track.w = interp1(k,w,t);
[track.x,track.y] = splitMatrix(points);
track.xy = points;
track.len = length(track.xy);
track = createBoundaries(track);
track = generateArcParam(track);
track.s