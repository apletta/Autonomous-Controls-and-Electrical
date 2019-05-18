clc
close all

fig = figure();
hold on

i = 1;
track = loadTrack('testTrack.mat',100,true);
car = TestCar([track.x(i);track.y(i);-30;1]);

n = 3; N = 8; dt = .5;

plot(track.x,track.y,'.r')
plot(track.bx,track.by,'.-k')
plot(track.yx,track.yy,'.-k')

his = [];

isLoopClosed = false;
totalTime = 0;
elapsedTime = 0;

pause

while true
    if ~ishandle(fig) || isLoopClosed
        break;
    end
    
    t = tic;
    tic
    %[car.state,isLoopClosed] = mpcOptimizer(track,car,n,N,dt);
    [car.state,isLoopClosed] = mpcNestedOptimizer(track,car,n,N,dt);
    t = toc(t);
    toc
    
    his(:,end+1) = car.state;
    
    plot(car.state(1),car.state(2),'.r','MarkerSize',15)
    
    totalTime = totalTime + dt;
    elapsedTime(end+1) = elapsedTime(end) + t;
    
    drawnow
end

disp('Lap Time: ' + string(round(totalTime(end),2)))
disp('Total Elapsed Time: ' + string(round(elapsedTime(end),4)))
disp('Mean Elapsed Time: ' + string(round(mean(diff(elapsedTime)),4)))

clf
hold on

plot(track.bx,track.by,'-k','LineWidth',2)
plot(track.yx,track.yy,'-k','LineWidth',2)

x = his(1,:); y = his(2,:); v = his(4,:);
patch([x nan], [y nan], [v nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);
patch([x nan], [y nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);plot(track.x,track.y,'.b')