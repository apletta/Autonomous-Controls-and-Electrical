function [k,ds] = distanceandcurvature(x,y)

% First derivative
dsx = diff(x);
dsy = diff(y);
ds = sqrt(dsx.^2+dsy.^2); % Distance along track
Tx = dsx./ds;
Ty = dsy./ds;

% Second derivative & curvature
ds2 = 0.5*(ds([end,1:end-1])+ds);
Hx = diff(Tx([end,1:end]))./ds2;
Hy = diff(Ty([end,1:end]))./ds2;

k = sqrt(diff(Hx).^2 + diff(Hy).^2);