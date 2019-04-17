function state = vehicleDynamicsOptimized2(track,car,N,dt)
    
    initState = car.state;
    width = 5;
    
    x0 = [0;0];
    A = [];
    B = [];
    Aeq = [];
    Beq = [];
    LB = [car.amin;car.amin];
    UB = [car.amax;car.amax];
    nonlcon = [];
    options = optimoptions('fmincon');
    options.MaxFunctionEvaluations = 50000;
    options.Algorithm = 'sqp';
    options.Display = 'none';
    options.OptimalityTolerance = 1e-6;
    %options.StepTolerance = 1e-15;
%     options.FiniteDifferenceStepSize = 1;

    result = fmincon(@objective,x0,A,B,Aeq,Beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    plot(state(1,:),state(2,:))
    state = state(:,2);
    pause(.1)
    
    function [c,ceq] = nonlincon(x)
        ax = x(1); ay = x(2);
        a = vecnorm([x(1);x(2)]);
        
        if a > car.amax
            ax = (ax / a) * car.amax;
            ay = (ay / a) * car.amax;
        elseif a < car.amin
            ax = (ax / a) * car.amin;
            ay = (ay / a) * car.amin;
        end
        
        c = [];
        ceq = [ax;ay];
    end
    
    function [cost,state] = objective(x)
        state = initState;
        
        for i = 1:N
            state(:,end+1) = getState(state(:,end), x);
        end
%         
        [~,d,~] = distance2curve(track.xy',[state(1,end),state(2,end)]);
%         
        [~,initialIndex] = min(sum(abs([track.x;track.y]-[state(1,1);state(2,1)])));
        [~,finalIndex] = min(sum(abs([track.x;track.y]-[state(1,end);state(2,end)])));
%         
        if d > (width / 2)
            cost = 100;
            return;
        elseif (finalIndex - initialIndex) < 0 || abs(finalIndex - initialIndex) > N*2
            cost = 10000;
            return;
        end
        
        s = arclength([track.x(initialIndex:finalIndex),state(1,end)],[track.y(initialIndex:finalIndex),state(2,end)]);
        
        cost = -sum(vecnorm(state(3:4,:)));
%         cost
        %cost = s;
    end

    function state = getState(state,u)
        %[x,y,vx,vy] = splitMatrix(state);
        %[ax, ay] = splitMatrix(u);
        
        MA = [1 0 dt 0;
            0 1 0 dt;
            0 0 1 0;
            0 0 0 1];
        
        MB = [dt^2/2 0;
            0 dt^2/2;
            dt 0;
            0 dt];
        
        state = MA * state + MB * u;
        
        v = vecnorm([state(3);state(4)]);
        if v > car.vmax
            state(3) = (state(3) / v) * car.vmax;
            state(4) = (state(4) / v) * car.vmax;
        elseif v < car.vmin
            state(3) = (state(3) / v) * car.vmin;
            state(4) = (state(4) / v) * car.vmin;
        end
    end
end