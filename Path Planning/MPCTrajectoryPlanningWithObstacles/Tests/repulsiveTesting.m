clc
close all

fig = figure;
hold on

track = loadTrack('testTrack2.mat',100,true);
car = RCCar([track.x(1);track.y(1);1;0]);
%repulsive = 
N = 10;
dt = 0.1;

stateHistory = [];

totalTime = 0;

hold on
plot(track.x,track.y,'.b')
plot(track.bx,track.by,'-k','LineWidth',2)
plot(track.yx,track.yy,'-k','LineWidth',2)
    
tic
while true
    
    if ~ishandle(fig)
        break;
    elseif totalTime > 1 && isLoopClosed(track,car.state)
        break;
    end
    
    tic
    car.state = RCCarOptimizer(track,car,N,dt);
    %car.state = vehicleDynamicsOptimized(track,car,N,dt);
    %car.state = pacmanCost(track,car,N,dt);
    %car.state = cheeseCost(track,car,N,dt);
    %car.state = speedMax(track,car,N,dt);
    toc
    
    stateHistory(:,end+1) = car.state;
    
    plot(car.state(1),car.state(2),'.r')
    
    drawnow
    totalTime = totalTime + dt;
end
toc
clf
hold on
v = vecnorm([stateHistory(3,:);stateHistory(4,:)]);
%v
patch([stateHistory(1,:) nan], [stateHistory(2,:) nan], [v nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);
patch([stateHistory(1,:) nan], [stateHistory(2,:) nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);plot(track.x,track.y,'.b')
plot(track.bx,track.by,'-k','LineWidth',2)
plot(track.yx,track.yy,'-k','LineWidth',2)

fprintf('Total Time : %s\n', int2str(totalTime));

saveStateHistory(stateHistory)

%plot(track.x,track.y,'.-r');