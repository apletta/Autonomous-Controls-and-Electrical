hold on
clc
tic
cp = loadData(500);
toc

track = Track(cp);
car = Car([track.getInitialPosition();0;0]);