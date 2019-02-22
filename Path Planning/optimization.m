function optimization(track, car)
    error = 10;
    if all(car.position+error >= track.obstacles.mids(car.current,:)') == 1 ...
        && all(car.position-error <= track.obstacles.mids(car.current,:)') == 1
            if car.current < track.length
                car.current = car.current + 1;
            else
                car.stats.path_completed = true;
                car.current = 1;
            end
    end
    a = track.obstacles.mids(car.current,:)' - car.position;
    car.acceleration = a;
    
    car.update();
end