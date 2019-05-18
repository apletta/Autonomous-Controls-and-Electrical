function state = speedMax(track,car,N,dt)
    
    initState = car.state';
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
    options.FiniteDifferenceStepSize = 1;

    result = fmincon(@objective,x0,A,B,Aeq,Beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    state = state(:,2)';
    
    function [cost,state] = objective(x)
        state = initState;
        vsum = 0;
        for i = 1:N
            state(:,end+1) = getState(state(:,end), x(:,i)');
            vsum = vsum - state(4,end);
        end
        [~,d,~] = distance2curve(track.xy,[state(1,end),state(2,end)]);
        if d > (width / 2)
            cost = 10000;
            return;
        end
        cost = d+vsum;
        %plot(state(1,:),state(2,:))
    end

    function state = getState(state,u)
        [x,y,psi,v] = splitMatrix(state');
        [a, delta] = splitMatrix(u);
        
        x_ = x + v*cosd(psi)*dt;
        y_ = y + v*sind(psi)*dt;
        psi_ = psi + (v / car.Lf) * delta * dt;
        v_ = v + a*dt;
        
        
        
        state = [x_,y_,psi_,v_]';
    end
end