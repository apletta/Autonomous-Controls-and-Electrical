function shortest_trajectory

% Clean up / initialize
clc; 
close all;

fig = figure();
hold on

track = Track('data/blue.txt','data/yellow.txt');
car = Car(track.obstacles.mids(1,:));

plot = true;

while 1
    %Loop breaker if exited
    if ~ishghandle(fig)
        break
    end
end

end