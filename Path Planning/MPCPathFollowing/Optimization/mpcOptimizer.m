function [state,isLoopClosed] = mpcOptimizer(track,car,n,N,dt)
    
    initState = car.state;
    width = 1.25;
    isLoopClosed = false;
    
    x0 = repmat([1;0],1,n);
    A = [];
    b = [];
    Aeq = [];
    beq = [];
    LB = repmat([car.amin;car.dmin],1,n);
    UB = repmat([car.amax;car.dmax],1,n);
    nonlcon = @nonlincon;
    options = optimoptions('fmincon');
    options.MaxFunctionEvaluations = 50000;
    options.Algorithm = 'sqp';
    options.Display = 'none';

    result = fmincon(@objective,x0,A,b,Aeq,beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    plot(state(1,:),state(2,:),'.-r','MarkerSize', 5);
    state = state(:,2);
    
    function [c,ceq] = nonlincon(x)
        ceq = [];
        c = [];
        
        state = initState;
        
        for i = 1:N
            if i < n
                v_ = state(4,end) + x(1,i)*dt;
                p_ = state(3,end) + x(2,i)*dt;
            else
                v_ = state(4,end) + x(1,end)*dt;
                p_ = state(3,end) + x(2,end)*dt;
            end
            y_ = state(2,end) + v_*sin(p_)*dt;
            x_ = state(1,end) + v_*cos(p_)*dt;
            state(:,end+1) = [x_,y_,p_,v_];
            
            c(end+1) = v_ - car.vmax;
            c(end+1) = v_ + car.vmin;
            c(end+1) = p_ - car.dmax;
            c(end+1) = p_ + car.dmin;
            
            [~,d,~,xyi] = distance2curve(track.xy',[state(1,end),state(2,end)]);
            c(end+1) = d - width;
            
            c(end+1) = (v_^2)/track.r(xyi) - car.lamax;
        end
    end
    
    function [cost,state] = objective(x)
        state = initState;
        
        for i = 1:N
            if i < n
                v_ = state(4,end) + x(1,i)*dt;
                p_ = state(3,end) + x(2,i)*dt;
            else
                v_ = state(4,end) + x(1,end)*dt;
                p_ = state(3,end) + x(2,end)*dt;
            end
            y_ = state(2,end) + v_*sin(p_)*dt;
            x_ = state(1,end) + v_*cos(p_)*dt;
            state(:,end+1) = [x_,y_,p_,v_];
        end
        
        [~,xyi] = min(sum(abs([track.x;track.y]-[state(1,2);state(2,2)])));
        [~,~,s2,~] = distance2curve(track.xy',[state(1,end),state(2,end)]);
        
        if xyi == track.len - 1
            disp('Loop has been closed')
            isLoopClosed = true;
        end
        
        cost = -s2;
    end
end