clc
close all

fig = figure();
hold on

track = loadTrack('testTrack1.mat',100,true);
car = TestCar([track.x(1);track.y(1);0;0]);

n = 3; N = 8; dt = .5;

plot(track.x,track.y,'.r')
plot(track.bx,track.by,'.-k')
plot(track.yx,track.yy,'.-k')

his = [];

isLoopClosed = false;

while true
    if ~ishandle(fig) || isLoopClosed
        break;
    end
    
    tic
    [car.state,isLoopClosed] = mpcOptimizer(track,car,n,N,dt);
    toc
    
    his(:,end+1) = car.state;
    
    plot(car.state(1),car.state(2),'.r','MarkerSize',2)
    
    drawnow
end

clf
hold on

plot(track.bx,track.by,'-k','LineWidth',2)
plot(track.yx,track.yy,'-k','LineWidth',2)

x = his(1,:); y = his(2,:); v = his(4,:);
patch([x nan], [y nan], [v nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);
patch([x nan], [y nan], [v nan], ...
    'EdgeColor','interp','LineWidth',5);plot(track.x,track.y,'.b')