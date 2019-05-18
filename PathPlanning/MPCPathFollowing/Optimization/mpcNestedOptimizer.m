function [state,isLoopClosed] = mpcNestedOptimizer(track,car,n,N,dt)
    
    initState = car.state;
    width = 1.25;
    isLoopClosed = false;
    
    xLast = []; % Last place computeall was called
    myceq = []; % Use for nonlinear inequality constraint
    myc = []; % Use for nonlinear equality constraint
    
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
    options.StepTolerance = 1e-1;
    options.OptimalityTolerance = 1;
    options.Display = 'none';

    result = fmincon(@objective,x0,A,b,Aeq,beq,LB,UB,nonlcon,options);
    [~,state] = objective(result);
    
    plot(state(1,:),state(2,:),'.-r','MarkerSize', 5);
    state = state(:,2);
    
    function [c,ceq] = nonlincon(x)
        ceq = [];
        c = [];
        
        state = initState;
        
        if ~isequal(x,xLast) % Check if computation is necessary
            [~,myceq,myc] = computeAll(x,state);
            xLast = x;
        end
        
        ceq = myceq;
        c = myc;
    end
    
    function [cost,state] = objective(x)
        state = initState;
        
        
        [state,myceq,myc,~,xyi,s] = computeAll(x,state);
        xLast = x;
        
        if xyi(2) == (track.len-1)
            disp('Loop has been closed')
            isLoopClosed = true;
        end
        
        cost = -sum(s);
    end
    
    function [state,ceq,c,d,xyi,s] = computeAll(x,state)
        ceq = [];
        c = [];
        xyi = 0;
        s = [];
        
        for i = 1:N
            ii = i;
            i(i>n) = n;
            
            v_ = state(4,end) + x(1,i)*dt;
            p_ = state(3,end) + x(2,i)*dt;
            y_ = state(2,end) + v_*sin(p_)*dt;
            x_ = state(1,end) + v_*cos(p_)*dt;
            state(:,end+1) = [x_,y_,p_,v_];
            
            c(end+1) = state(4,i) - car.vmax;
            c(end+1) = state(4,i) + car.vmin;
            %c(end+1) = state(3,i) - car.dmax;
            %c(end+1) = state(3,i) + car.dmin;
            c(end+1) = atan((1/2)*(5/2)*(car.lamax/state(4,i)^2)) - abs(state(3,i));
            
            [~,d,s(end+1),xyi(end+1)] = distance2curve(track.xy',[state(1,ii),state(2,ii)]);
            c(end+1) = d - width;
            
            c(end+1) = (state(4,i)^2)/track.r(xyi(end)) - car.lamax;
        end
    end
end