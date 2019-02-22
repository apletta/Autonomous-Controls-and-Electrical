classdef Car < handle
    
    properties
        position
        velocity
        acceleration
        velocity_limit
        acceleration_limit
        magnitude
        current
        time_interval
        stats
    end
    
    methods
        function obj = Car(initPos)
            obj.position = initPos';
            obj.velocity = zeros(2, 1);
            obj.acceleration = zeros(2, 1);
            obj.velocity_limit = 5;
            obj.acceleration_limit = 5;
            obj.magnitude = .5;
            obj.current = 1;
            obj.time_interval = .01;
            obj.initiateStats();
        end
        
        function initiateStats(obj)
            obj.stats = struct;
            obj.stats.path = [];
            obj.stats.path_completed = false;
            obj.stats.lastPos = obj.position;
            obj.stats.lastVel = obj.velocity;
            obj.stats.lastAcc = obj.acceleration;
            obj.stats.distance = 0;
            obj.stats.position = [];
            obj.stats.velocity = [];
            obj.stats.acceleration = [];
            obj.stats.angles = [];
            obj.stats.iterations = [];
        end
        
        function completed_lap(obj)
            error = 10;
            for point = obj.stats.path(:,1:end-1)
                if all(obj.position+error >= point) == 1 && all(obj.position-error <= point) == 1
                    obj.stats.path_completed = true;
                    return;
                end
            end
        end
        
        function update(obj)
            obj.velocity = obj.velocity * obj.magnitude + obj.acceleration;
            obj.position = obj.position + obj.velocity * obj.magnitude;
            if norm(obj.velocity) > obj.velocity_limit
                obj.velocity = obj.velocity/(norm(obj.velocity)*obj.velocity_limit);
            end
            if norm(obj.acceleration) > obj.acceleration_limit
                obj.acceleration = obj.velocity/(norm(obj.acceleration)*obj.acceleration_limit);
            end
            obj.stats.path = [obj.stats.path obj.position];
            obj.stats.distance = obj.stats.distance + pdist([obj.position';obj.stats.lastPos']);
            obj.stats.position = [obj.stats.position norm(obj.position)];
            obj.stats.velocity = [obj.stats.velocity norm(obj.velocity)];
            obj.stats.acceleration = [obj.stats.acceleration norm(obj.acceleration)];
            obj.stats.iterations = [obj.stats.iterations length(obj.stats.iterations)];
            obj.stats.lastPos = obj.position;
            obj.stats.lastVel = obj.velocity;
            obj.stats.lastAcc = obj.acceleration;
        end
        
        function draw(obj)
            width = .5;
            height = 1;
            d = obj.velocity / norm(obj.velocity);
            R = [d [-d(2); d(1)]];
            vehicleRectangle = R*[height 0;0 width]*[1 1 -1 -1;1 -1 -1 1]+repmat(obj.position(1:2,1),1,4);
            fill(vehicleRectangle(1,:),vehicleRectangle(2,:),[0 0 0]);
            if ~isempty(obj.stats.path)
                plot(obj.stats.path(1,:), obj.stats.path(2,:), '-r');
            end
            %quiver(obj.position(1), obj.position(2), obj.velocity(1), obj.velocity(2))
            %quiver(obj.position(1), obj.position(2), obj.acceleration(1), obj.acceleration(2))
        end
        
        function draw_completed_path(obj)
            if ~isempty(obj.stats.path)
                obj.stats.path = [obj.stats.path obj.stats.path(:,1)];
                plot(obj.stats.path(1,:), obj.stats.path(2,:), '-r');
            end
        end
    end
end

