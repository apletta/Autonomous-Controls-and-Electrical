function car = RCCar(state)

    if exist('state')
        car.state = state;
    else
        car.state = [0;0;0;0];
    end
    
    car.vmin = -4;
    car.vmax = 4;
    
    car.amin = -10;
    car.amax = 10;
    
    car.dmin = -60;
    car.dmax = 60;
    
    car.Lf = 10;
    car.Lr = 10;
    