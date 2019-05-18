function state = RCCarOptimizer(track,car,N,dt)
    
    initState = car.state;
    width = 2;
    
    v = vecnorm([initState(3);initState(4)]);
    x0 = repmat([0;0],1,N);
    A = [];
    B = [];
    Aeq = [];
    Beq = [];
    LB = repmat([car.amin;car.amin],1,N);
    UB = repmat([car.amax;car.amax],1,N);
    nonlcon = [];
    options = optimoptions('fmincon');
    options.MaxFunctionEvaluations = 50000;
    options.Algorithm = 'sqp';
    options.Display = 'none';
    %options.FiniteDifferenceStepSize = 10;
    %options.StepTolerance = 1e-15;

    result = fmincon(@objective,x0,A,B,Aeq,Beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    plot(state(1,:),state(2,:))
    state = state(:,2);
    
    function [c,ceq] = nonlincon(x)
        ceq = [];
        c(1) = vecnorm([x(1);x(2)]) - 1;
    end
    
    function [cost,state] = objective(x)
        state = initState;
        
        for i = 1:N
            %state(:,end+1) = MA * state(:,end) + MB * x(:,i);
            state(:,end+1) = getState(state(:,end), x(:,i));
        end
            [~,d,s] = distance2curve(track.xy',[state(1,end),state(2,end)]);
            if d > (width / 2)
                cost = 100;
                return;
            end
%         
        %[~,initialIndex] = min(sum(abs([track.x;track.y]-[state(1,1);state(2,1)])));
        %[~,finalIndex] = min(sum(abs([track.x;track.y]-[state(1,end);state(2,end)])));
%         
%         if d > (width / 2)
%             cost = 100;
%             return;
% %         elseif (finalIndex - initialIndex) <= 0 || abs(finalIndex - initialIndex) > N*2
% %             cost = 10000;
% %             return;
%         end
        
        %s = arclength([track.x(initialIndex:(finalIndex))],[track.y(initialIndex:(finalIndex))]);
        %s = sum(track.s(initialIndex:finalIndex));
        
        cost = -s(end);
    end

    function state = getState(state,u)
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