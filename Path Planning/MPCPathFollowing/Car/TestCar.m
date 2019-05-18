function car = TestCar(state)

    if exist('state','var')
        car.state = state;
    else
        car.state = [0;0;0;0];
    end
    
    car.vmin = -25;
    car.vmax = 25;
    
    car.amin = -1;
    car.amax = 1;
    
    car.lamax = 1;
    
    car.dmin = -pi/3;
    car.dmax = pi/3;
    
    car.Lf = 10;
    car.Lr = 10;
    car.L = 20;
    