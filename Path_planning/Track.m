classdef Track < handle
    
    properties
        length
        blue
        yellow
        colors
        obstacles
    end
    
    methods
        function obj = Track(blue_filename, yellow_filename)
            obj.blue = split_data(blue_filename);
            obj.yellow = split_data(yellow_filename);
            obj.colors = jet(length(obj.blue));
            obj.length = obj.blue.length;
            obj.initializeTrack();
        end
        
        function initializeTrack(obj)
            obj.obstacles = struct;
            obj.obstacles.width = 5;
            obj.obstacles.blue = obj.blue;
            obj.obstacles.yellow = obj.yellow;
            obj.obstacles.length = obj.blue.length;
            obj.obstacles.mids = obj.compute_midpoints();
            obj.obstacles.vectors = obj.compute_vectors();
            obj.obstacles.angles = obj.compute_angles();
            obj.obstacles.points = [obj.blue.points'; obj.yellow.points'];
            %obj.fix_mids()
        end
        
        function fix_mids(obj)
            for i = 1:obj.length
                if mod(i,2) == 0
                    obj.obstacles.mids(i) = obj.obstacles.mids(i) + .1;
                end
            end
        end
        
        function mids = compute_midpoints(obj)
            mids = (obj.blue.points(:,:) + obj.yellow.points(:,:))/2;
        end
        
        function angles = compute_angles(obj)
            
            slopes = (obj.yellow.y - obj.blue.y) ./ (obj.yellow.x - obj.blue.x);

            slopes(isinf(slopes)) = 0;

            angles = atan((slopes(2:end) - slopes(1:end-1)) ./...
                (1 + slopes(1:end-1) .* slopes(2:end)));
            
        end
        
        function vectors = compute_vectors(obj) 
            mids = obj.obstacles.mids';
            vectors = [mids(1,2:end) - mids(1,1:end-1); ...
                mids(2,2:end) - mids(2,1:end-1)]';
        end
            
        function slope = line_slope(l1, l2)

            delta_y = l1(2) - l2(2);
            delta_x = l1(1) - l2(1);
            if delta_x == 0
                delta_x = 0.00001;
            end

            slope = delta_y / delta_x;

        end
        
        function plot(obj)
            s = scatter(obj.blue.x, obj.blue.y, 50, 'filled', 'b^', ...
                'MarkerEdgeColor', 'k');
            obj.color_changer(s);
            s = scatter(obj.yellow.x, obj.yellow.y, 50, 'filled', 'y^', ...
                'MarkerEdgeColor', 'k');
            obj.color_changer(s);
            scatter(obj.obstacles.mids(:,1), obj.obstacles.mids(:,2), 100, 'filled', '.k', ...
                'MarkerEdgeColor', 'k');
            %quiver(obj.obstacles.mids(1:end-1,1), obj.obstacles.mids(1:end-1,2), obj.obstacles.vectors(:,2), -obj.obstacles.vectors(:,1));
            %quiver(obj.obstacles.mids(1:end-1,1), obj.obstacles.mids(1:end-1,2), obj.obstacles.vectors(:,1), obj.obstacles.vectors(:,2));
            %pts=[fliplr(obj.blue.points') obj.blue.points(end,:)' obj.yellow.points' obj.yellow.points(1,:)'];
            %fill(pts(1,:), pts(2,:),[1 1 1]*.8,'EdgeAlpha',0);
        end
        
        function color_changer(obj, scatter)
            data = scatter.CData;
            data = repmat(data, [obj.length 1]);
            data(1,:) = [1 0 0];
            scatter.CData = data;
        end
    end
end

