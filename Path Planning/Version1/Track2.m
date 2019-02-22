classdef Track2 < handle
    properties
        blue
        yellow
        mids
        vectors
        angles
        distances
        widths
        
        checkpoints
        
        len
        
        num
        
        traj
        
        friction
    end
    
    methods
        %% CONSTRUCTOR
        function self = Track2()
            tic
            blue_path = 'data/blue2.csv';
            yellow_path = 'data/yellow2.csv';
            self.num = 10;
            
            self.blue = load_data(blue_path,1);
            self.yellow = load_data(yellow_path,1);
            
            self.init_properties();
            
            self.init_checkpoints();
            
            self.add_checkpoints();
            toc
            self.draw();
            
        end
        
        %% INITIALIZERS
        
        function init_properties(self)
            self.mids = self.compute_mids(self.blue,self.yellow);
            
            self.vectors = self.compute_vectors(self.mids);
            
            [~,~,self.angles,self.distances] = path_radius(self.mids.x,self.mids.y);
            
            
            self.angles = self.compute_angles(self.vectors);
            %self.distances = self.compute_distances(self.vectors);
            self.widths = self.compute_widths(self.blue,self.yellow);
            
            self.len = length(self.angles);
        end
        
        function init_checkpoints(self)
            self.checkpoints = struct;
            self.checkpoints.blue = self.blue.points(:,1);
            self.checkpoints.yellow = self.yellow.points(:,1);
            self.checkpoints.mids = self.mids.points(:,1);
            self.checkpoints.yaw = self.angles(end);
            self.checkpoints.forward_vectors = self.vectors.points(1:2,1) ...
                ./ self.num;
        end
        
        %% CHECKPOINT CREATION
        function add_checkpoints(self)
            diffwidths = diff([self.widths, self.widths(1)]);
            for i = 1:self.len
                kappa = self.angles(i) / self.distances(i);
                ds = self.distances(i) / self.num;
                width = self.widths(i);
                dw = diffwidths(i) / self.num;
                
                for ii=1:self.num
                    self.checkpoints(end+1).yaw = self.checkpoints(end).yaw + kappa * ds;
                    c = cos(self.checkpoints(end).yaw);
                    s = sin(self.checkpoints(end).yaw);
                    f = [c;s];
                    n = [-s;c];
                    self.checkpoints(end).mids = self.checkpoints(end-1).mids + f * ds;
                    self.checkpoints(end).blue = self.checkpoints(end).mids + n * width/2;
                    self.checkpoints(end).yellow = self.checkpoints(end).mids - n * width/2;
                    self.checkpoints(end).forward_vectors = f;
                    width = width + dw;
                end
            end
        end
        
        %% HELPER FUNCTIONS
        function mids = compute_mids(~, blue, yellow)
            mids.points = (blue.points + yellow.points)/2;
            mids.x = mids.points(1,:);
            mids.y = mids.points(2,:);
            mids.length = length(mids.points);
        end
        
        function vectors = compute_vectors(~, path)
            vectors.points = [diff(path.points,1,2); ...
                zeros(1,path.length-1)];
            vectors.x = vectors.points(1,:);
            vectors.y = vectors.points(2,:);
            vectors.length = length(vectors.points);
        end

        function angles = compute_angles(~, vectors)
            v1 = vectors.points(:,1:end);
            v2 = [vectors.points(:,2:end) vectors.points(:,1)];
            vn = [0;0;1];
            angles = acos(dot(v1,v2) ./ (vecnorm(v1) .* vecnorm(v2)));
            n = dot(cross(v1,v2),repmat(vn,1,vectors.length)) < 0;
            angles(n) = -angles(n);
            angles(isnan(angles)) = 0;
        end
        
        function distances = compute_distances(~, vectors)
            distances = vecnorm(vectors.points);
        end
        
        function widths = compute_widths(~,blue,yellow)
            widths = vecnorm(blue.points-yellow.points);
        end
        
        %% TRACK PLOTTER
        function draw(self)
            hold on
            center = [self.checkpoints.mids];
            left = [self.checkpoints.blue];
            right = [self.checkpoints.yellow];
            v = [self.checkpoints.forward_vectors];
            plot(center(1,:),center(2,:));
            plot(left(1,:),left(2,:));
            plot(right(1,:),right(2,:));
            quiver(center(1,:),center(2,:),v(1,:),v(2,:))
            
            plot(self.mids.x,self.mids.y,'^m')
            plot(self.blue.x,self.blue.y,'^b')
            plot(self.yellow.x,self.yellow.y,'^r')
        end
    end
end

