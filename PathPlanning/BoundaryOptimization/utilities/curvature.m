function [Hx,Hy] = curvature(x,y)
    % First derivative
    dsx = diff(x);
    dsy = diff(y);
    ds = sqrt(dsx.^2+dsy.^2);
    Tx = dsx./ds;
    Ty = dsy./ds;
    
    % Second derivative & curvature
    ds2 = 0.5*(ds([end,1:end-1])+ds);
    Hx = diff(Tx([end,1:end]))./ds2;
    Hy = diff(Ty([end,1:end]))./ds2;
    
    x = x(1:end-1);
    y = y(1:end-1); % remove repeated point
    
    quiver(x,y,-Ty,Tx)
    
    dx = diff(Hx).^2;
    dy = diff(Hy).^2;
    
    k = sqrt(dx + dy);
        