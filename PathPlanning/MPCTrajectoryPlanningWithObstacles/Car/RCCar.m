function car = RCCar(state)

    if exist('state')
        car.state = state;
    else
        car.state = [0;0;0;0];
    end
    
    car.vmin = -.1;
    car.vmax = .1;
    
    car.amin = -.1;
    car.amax = .1;
    
    car.dmin = -60;
    car.dmax = 60;
    
    car.Lf = 10;
    car.Lr = 10;
    