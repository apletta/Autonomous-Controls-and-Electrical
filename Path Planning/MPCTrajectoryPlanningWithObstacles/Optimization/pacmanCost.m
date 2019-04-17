function state = pacmanCost(track,car,N,dt)
    
    initState = car.state;
    width = 5;
    
    x0 = repmat([1;0],1,N);
    A = [];
    B = [];
    Aeq = [];
    Beq = [];
    LB = repmat([car.amin;car.dmin],1,N);
    UB = repmat([car.amax;car.dmax],1,N);
    nonlcon = [];
    options = optimoptions('fmincon');
    options.MaxFunctionEvaluations = 50000;
    options.Algorithm = 'sqp';
    options.Display = 'none';
    %options.FiniteDifferenceStepSize = 1;

    result = fmincon(@objective,x0,A,B,Aeq,Beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    plot(state(1,:),state(2,:))
    state = state(:,2);
    
    function [cost,state] = objective(x)
        state = initState;
        
        for i = 1:N
            state(:,end+1) = getState(state(:,end), x(:,i));
        end
        
        %vsum = sum(abs(state(3,:)));
        
        [~,d,~] = distance2curve(track.xy',[state(1,end),state(2,end)]);
        
        [~,initialIndex] = min(sum(abs([track.x;track.y]-[state(1,1);state(2,1)])));
        [~,finalIndex] = min(sum(abs([track.x;track.y]-[state(1,end);state(2,end)])));
        
        if d > (width / 2)
            cost = 10000;
            return;
        elseif (finalIndex - initialIndex) < 0 || abs(finalIndex - initialIndex) > N*2
            cost = 10000;
            return;
        end
        
        s = arclength(track.x(initialIndex:finalIndex),track.y(initialIndex:finalIndex));
        
        cost = d-s;
    end

    function state = getState(state,u)
        [x,y,psi,v] = splitMatrix(state);
        [a, delta] = splitMatrix(u);
        
        deltamax = atand((1/2)*car.Lf/2*1.5/(v^2));
        if abs(delta) > abs(deltamax)
            delta = deltamax;
        end
        
        x_ = x + v*cosd(psi)*dt;
        y_ = y + v*sind(psi)*dt;
        psi_ = psi + (v / car.Lf) * delta*dt;
        v_ = v + a*dt;
        
        if v_ > car.vmax
            v_ = car.vmax;
        elseif v_ < car.vmin
            v_ = car.vmin;
        end
        
%         if psi_ > car.dmax
%             psi_ = car.dmax;
%         elseif psi_ < car.dmin
%             psi_ = car.dmin;
%         end
        
        state = [x_;y_;psi_;v_];
    end
end