%% SPLIT DATA
function obstacles = split_data(file_name)

file = fopen(file_name,'r');
data = textscan(file, '%f %f');

obstacles = struct;
obstacles.length = length(data{1});
obstacles.x = [];
obstacles.y = [];
obstacles.points = [];
obstacles.mid = [];

obstacles = retrieve_points(data, obstacles);
obstacles.points = [obstacles.x.'; obstacles.y.'].';

end

%% POINT RETRIEVAL FROM FILE
function obstacles = retrieve_points(data, obstacles)

obstacles.x = data{1,1}(:);
obstacles.y = data{1,2}(:);

end