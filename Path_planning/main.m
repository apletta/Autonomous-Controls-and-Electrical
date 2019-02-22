function main

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
    
    if car.stats.path_completed
        if ~plot
            plotOptimization(track, car);
        end
        break;
    end
    
    optimization(track, car);
    %time_based_optimization(track, car);
    
    if plot
        plotOptimization(track, car);
        pause(.000000001)
    end
end

end