clear
clc
clf
hold on

%tic

tracknum = '2';
numofpoints = 100;
algorithmToRun = 'normalFromMidPoint';

track = Track(tracknum,numofpoints,algorithmToRun);

if true
    if true
        traj = trajectoryOptimization(track);
    else
        traj = [];
    end

    %plotOptimization(track,traj,...
    %    'obstacles');
end
%toc
