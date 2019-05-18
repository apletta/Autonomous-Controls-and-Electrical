clear
clc
clf
hold on

%tic

tracknum = '';
numofpoints = 100;
algorithmToRun = 'normalIntersection';

track = Track(tracknum,numofpoints,algorithmToRun);

if true
    if true
        traj = trajectoryOptimization(track);
    else
        traj = [];
    end

    plotOptimization(track,traj,...
        'obstacles', 'trajectory', 'checkpoints');
end
%toc
