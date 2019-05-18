function plotOptimization(track, car)
    clf
    hold on
    if(car.stats.path_completed)
        car.draw_completed_path();
        track.plot();
        fig = figure();
        subplot(2,2,1)
        plot(car.stats.iterations, car.stats.position,'Color', [.2 .8 .5]);
        title('Position');
        subplot(2,2,2);
        plot(car.stats.iterations, car.stats.velocity,'-b');
        title('Velocity');
        subplot(2,2,3)
        plot(car.stats.iterations, car.stats.acceleration,'-m');
        title('Acceleration');
        subplot(2,2,4)
        %plot(car.stats.iterations, car.stats.angles,'-m');
        title('Angles');
        time = car.stats.distance/(norm(car.stats.velocity))
    else
        car.draw();
        track.plot();
    end

end