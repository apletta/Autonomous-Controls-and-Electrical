clc

hold on
num = 100;
%[b,y,m] = loadData('2',num);

p = spcrv([b.p,y.p],10);
plot(b.x,b.y,'b-')
plot(p(1,:),p(2,:),'.r')