function track = track_creation(obOne, obTwo)

track = struct;
track.obstacles.blue = obOne;
track.obstacles.yellow = obTwo;
track.obstacles.length = obOne.length;
track.obstacles.mids = compute_midpoints(obOne, obTwo);
track.obstacles.angles = compute_angles(obOne, obTwo);

end

%% MIDPOINT COMPUTATION
function mids = compute_midpoints(obOne, obTwo)

mids = (obOne.points(:,:) + obTwo.points(:,:))/2;

end
%% ANGLE COMPUTATION
function angles = compute_angles(obOne, obTwo)

line_slope(obOne.points(1,:), obTwo.points(1,:));

slopes = (obTwo.y - obOne.y) ./ (obTwo.x - obOne.x);

slopes(isinf(slopes)) = 0;

angles = atan((slopes(2:end) - slopes(1:end-1)) ./...
    (1 + slopes(1:end-1) .* slopes(2:end)));

end

function slope = line_slope(l1, l2)

delta_y = l1(2) - l2(2);
delta_x = l1(1) - l2(1);
if delta_x == 0
    delta_x = 0.00001;
end

slope = delta_y / delta_x;

end

function angle = line_angle(l1, l2)

tan_theta = (l2 - l1)/ (1 + l1*l2);
angle = atan(tan_theta);

end