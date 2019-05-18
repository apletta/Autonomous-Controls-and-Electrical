classdef Track < handle
    % This class represents the a track object.
    % Implements algorithms to describe the track for subsequent
    % trajectory optimization. The description is a set of points that
    % describes a connection between an inner boundary and an outer
    % boundary.
    %
    % A track description is interperated as a matrix of checkpoints in the
    % following form:
    % [x11, x12, x13, x14 ...;
    %  y11, y12, y13, y14 ...;
    %  x21, x22, x23, x24 ...;
    %  y21, y22, y23, y24 ...]
    % These checkpoints are then used to optimize an optimal trajectory
    % through the entirety of the track (see trajectoryOptimization.m)
    
    properties
        bluePoints,blueX,blueY,blueFunction
        yellowPoints,yellowX,yellowY,yellowFunction
        midPoints,midX,midY
        checkpoints
        numOfPoints
    end
    
    methods
        %% CONSTRUCTOR
        function self = Track(trackNum,numOfPoints,algorithmToRun)
            %Track Construct an instance of this class
            %   Takes a tracknum and numofpoints as inputs
            %   Loads track data and sets class variables
            %   Runs initialization functions
            
            self.initializeTrack(trackNum,numOfPoints);
            
            self.initializeTrackConnections(algorithmToRun);
        end
        
        %% INITIALIZATION FUNCTIONS
        function initializeTrack(self,trackNum,numOfPoints)
            %  Initializes Track data
            %  Loads track data into class variables
            %  Takes a trackNum to load data from and number of points to
            %  spline
            
            % Creates file path name from trackNum
            bluePath = sprintf('blue%s.csv',trackNum);
            yellowPath = sprintf('yellow%s.csv',trackNum);
            
            % Loads track data from specified csv files
            [yp,yx,yy,yf] = loadData(yellowPath,numOfPoints);
            self.yellowPoints = yp; self.yellowFunction = yf;
            self.yellowX = yx; self.yellowY = yy;
            
            [bp,bx,by,bf] = loadData(bluePath,numOfPoints);
            self.bluePoints = bp; self.blueFunction = bf;
            self.blueX = bx; self.blueY = by;
            
            [self.midPoints,self.midX,self.midY] = self.computeMidPoints(...
                self.yellowPoints,self.bluePoints);
            
            self.numOfPoints = numOfPoints;
        end
        
        function initializeTrackConnections(self, algorithmToRun)
            % Runs track description connection functions
            % Takes a string option that chooses algorithm type
            
            switch(algorithmToRun)
                case 'indices'
                    self.indices()
                case 'normalClosest'
                    self.normalClosest()
                case 'normalIntersection'
                    self.normalIntersection()
                case 'normalIntersectionFromCenter'
                    self.normalIntersectionFromCenter()
                case 'indicesFromFunction'
                    self.indicesFromFunction()
                case 'normalIntersectionFromFunction'
                    self.normalIntersectionFromFunction()
                case 'normalFromMidPoint'
                    self.normalFromMidPoint()
                otherwise
                    error('algorithmToRun specified does not exist: %s', ...
                        algorithmToRun)
            end
            
            % self.organizeCheckpoints()
        end
       
        %% TRACK DESCRIPTION FUNCTIONS
        function indices(self)
            % Track description function
            % Creates connections based on the indicies of the boundary
            % matrices
            
            % Creates checkpoint matrix
            self.checkpoints = [self.bluePoints;self.yellowPoints];
        end
        function normalClosest(self)
            % Track description function
            % Creates connections based on the closest point opposite of
            % the normal vector from the yellow boundary path
            
            % Boundary points
            boundaryX = self.yellowX; boundaryY = self.yellowY;
            
            % Computes normal unit vectors from path points
            [~,unx,uny] = self.computeNormals(boundaryX,boundaryY);
            
            % Create new vector with desired distance 
            d = removeLastFromMatrix( ...
                self.distanceOfPoints(self.bluePoints,self.yellowPoints));
            nx = unx .* d;
            ny = uny .* d;
            
            % Calculates end point of line intersection
            [x,y] = removeLastFromMatrix(boundaryX,boundaryY);
            x2 = x + nx;
            y2 = y + ny;
            
            %plot([x1;x2],[y1;y2])
            
            % Removes repeating value from boundary points
            [x1,y1] = removeLastFromMatrix(self.blueX,self.blueY);
            
            x = [];
            y = [];
            
            % Finds shortest distance between the end of the normal line
            % segment and a point along the other boundary spline.
            for i = 1:self.numOfPoints
                % Computes distance
                d = sqrt((x2(i)-x1).^2 + (y2(i)-y1).^2);
                
                % Finds minimum distance
                x(1+end) = x1(d==min(d));
                y(1+end) = y1(d==min(d));
            end
            
            % Creates checkpoint matrix
            self.checkpoints = [removeLastFromMatrix([boundaryX;boundaryY]);x;y];
        end
        
        function normalIntersection(self)
            % Track description function.
            % Creates connections based on the intersection of the normal
            % vector with the opposite boundary.
            
            % Boundary points
            boundaryX = self.yellowX; boundaryY = self.yellowY;
            
            % Computes normal unit vectors from path points
            [~,unx,uny] = self.computeNormals(boundaryX,boundaryY);
            
            % Create new vector with desired distance 
            d = 100;
            nx = unx .* d;
            ny = uny .* d;
            
            % Calculates end point of line intersection
            [x,y] = removeLastFromMatrix(boundaryX,boundaryY);
            x2 = x + nx;
            y2 = y + ny;
            
            %plot([x1;x2],[y1;y2])
            
            % Removes repeating value from boundary points
            [x1,y1] = removeLastFromMatrix(self.yellowX,self.yellowY);
            
            x = [];
            y = [];
            
            % Finds shortest distance between the end of the normal line
            % segment and a point along the other boundary spline.
            for i = 1:self.numOfPoints
                [x0,y0] = intersections([x1(i),x2(i)],[y1(i),y2(i)], ...
                    self.blueX,self.blueY);
                
                % Computes distance
                d = sqrt((x1(i)-x0).^2 + (y1(i)-y0).^2);
                
                % Finds minimum distance of the interesections
                x(1+end) = x0(d==min(d));
                y(1+end) = y0(d==min(d));
            end
            
            % Creates checkpoint matrix
            self.checkpoints = [removeLastFromMatrix([boundaryX;boundaryY]);x;y];
            self.checkpoints = addInitialPoint(self.checkpoints);
        end
        
        function normalIntersectionFromCenter(self)
            % Track description function
            % Creates connections based on the normal intersection from the
            % mid points of two boundary paths
            
            bx1 = []; by1 = [];
            bx2 = []; by2 = [];
            
            for i = 1:2
                
                % Boundary points
                if i == 1
                    boundaryX = self.yellowX; boundaryY = self.yellowY;
                else
                    boundaryX = self.blueX; boundaryY = self.blueY;
                end
                    
                % Computes normal unit vectors from path points
                % Flips direction of normals depending on boundary
                [~,unx,uny] = self.computeNormals(self.midX,self.midY,i-1);
                
                % Create new vector with desired distance
                d = 10;
                nx = unx .* d;
                ny = uny .* d;
                
                % Calculates end point of line intersection
                [x,y] = removeLastFromMatrix(self.midX,self.midY);
                x2 = x + nx;
                y2 = y + ny;
                
                % Removes repeating value from boundary points
                [x1,y1] = removeLastFromMatrix(boundaryX,boundaryY);
                
                plot(self.midX,self.midY)
                plot(self.blueX,self.blueY,'b')
                plot(self.yellowX,self.yellowY,'r')
                plot([x;x2],[y;y2])
                
                x = [];
                y = [];
                
                % Finds shortest distance between the end of the normal line
                % segment and a point along the other boundary spline.
                for i = 1:self.numOfPoints
                    [x0,y0] = intersections([x1(i),x2(i)],[y1(i),y2(i)], ...
                        self.blueX,self.blueY);
                    
                    % Computes distance
                    d = sqrt((x1(i)-x0).^2 + (y1(i)-y0).^2);
                    
                    % Finds minimum distance of the interesections
                    x(1+end) = x0(d==min(d));
                    y(1+end) = y0(d==min(d));
                end
            end
            
            % Creates checkpoint matrix
            self.checkpoints = [removeLastFromMatrix([boundaryX;boundaryY]);x;y];
            self.checkpoints = addInitialPoint(self.checkpoints);
        end
        
        function indicesFromFunction(self)
            % Track description function
            % Creates connections based on the indicies from the spline
            % function
            
            blueDataLength = self.blueFunction.pieces;
            dp = (blueDataLength) / self.numOfPoints;
            t = 1:dp:blueDataLength+1;
            blue = fnval(self.blueFunction,t);
            
            yellowDataLength = self.yellowFunction.pieces;
            dp = (yellowDataLength) / self.numOfPoints;
            t = 1:dp:yellowDataLength+1;
            yellow = fnval(self.yellowFunction,t);
            self.checkpoints = [blue;yellow];
            
            %cdv = fnval(fnder(self.blueFunction), t);
            %quiver(blue(1,:),blue(2,:), cdv(2,:),-cdv(1,:));
        end
        
        function normalIntersectionFromFunction(self)
            % Track description function
            % Creates checkpoints based on the interesection between the
            % normal vector of one boundary and the other boundary
            
            blueDataLength = self.blueFunction.pieces;
            dp = (blueDataLength) / self.numOfPoints;
            t = 1:dp:blueDataLength+1;
            blue = fnval(self.blueFunction,t);
            
            yellowDataLength = self.yellowFunction.pieces;
            dp = (yellowDataLength) / self.numOfPoints;
            t = 1:dp:yellowDataLength+1;
            yellow = fnval(self.yellowFunction,t);
            
            mids = fncmb(fncmb(self.yellowFunction,'+', self.blueFunction),.5);
            %fnplt(mids)
            cdv = fnval(fnder(mids), t);
            mids = fnval(mids,t);
            [mX, mY] = matrixTo1D(mids);
            %quiver(mids(1,:),mids(2,:), cdv(2,:),-cdv(1,:));
            
            [tx,ty] = matrixTo1D(cdv);
            nx = ty;
            ny = -tx;
            %quiver(mX, mY, nx,ny)
            
            x1 = mX; y1 = mY;
            
            x2 = mX + nx*2;
            y2 = mY + ny*2;
            
            %plot([mX;x2],[mY;y2])
            
            x = [];
            y = [];
            
            for i = 1:self.numOfPoints
                [x0,y0] = intersections([x1(i),x2(i)],[y1(i),y2(i)], ...
                    self.yellowX,self.yellowY);
                
                % Computes distance
                d = sqrt((x1(i)-x0).^2 + (y1(i)-y0).^2);
                
                if isempty(x0) || isempty(y0)
                    x(1+end) = self.yellowX(i);
                    y(1+end) = self.yellowY(i);
                else
                    % Finds minimum distance of the interesections
                    x(1+end) = x0(d==min(d));
                    y(1+end) = y0(d==min(d));
                end
            end
            
            firstCheckpoints = [x;y];
            
            x = [];
            y = [];
            
            [tx,ty] = matrixTo1D(cdv);
            nx = -ty;
            ny = tx;
            %quiver(mX, mY, nx,ny)
            
            x2 = mX + nx*2;
            y2 = mY + ny*2;
            
            for i = 1:self.numOfPoints
                [x0,y0] = intersections([x1(i),x2(i)],[y1(i),y2(i)], ...
                    self.blueX,self.blueY);
                
                % Computes distance
                d = sqrt((x1(i)-x0).^2 + (y1(i)-y0).^2);
                
                if isempty(x0) || isempty(y0)
                    x(1+end) = self.blueX(i);
                    y(1+end) = self.blueY(i);
                else
                    % Finds minimum distance of the interesections
                    x(1+end) = x0(d==min(d));
                    y(1+end) = y0(d==min(d));
                end
            end
            
            % Creates checkpoint matrix
            self.checkpoints = [x;y;firstCheckpoints];
            self.checkpoints = addInitialPoint(self.checkpoints);
        end
        
        function normalFromMidPoint(self)
            fnplt(fncmb(fncmb(self.yellowFunction,'+',self.blueFunction),.5));
            fnplt(self.blueFunction)
            fnplt(self.yellowFunction)
        end
        
        %% HELPER FUNCTIONS
        function [np,nx,ny] = computeNormals(~,x,y,flipDirection)
            % Computes the normal vectors of the given xy path
            
            dsx = diff(x);
            dsy = diff(y);
            ds = sqrt(dsx.^2+dsy.^2);
            Tx = dsx./ds;
            Ty = dsy./ds;
            
            % Checks if the direction needs to be flipped
            if nargin == 3 || ~flipDirection
                np = [-Ty;Tx];
            else
                np = [Ty;-Tx];
            end
            
            [nx,ny] = matrixTo1D(np);
        end
        
        function d = distanceOfPoints(~,p1,p2)
            % Computes the distance between two paths
            
            [x1,y1,x2,y2] = matrixTo1D([p1;p2]);
            d = sqrt((x2-x1).^2 + (y2-y1).^2);
        end
        
        function [points,x,y] = computeMidPoints(~,p1,p2)
            % Computes the mid points between two specified xy paths
            
            points = (p1 + p2)/2;
            [x,y] = matrixTo1D(points);
        end
        
        function organizeCheckpoints(self)
            [x1,y1,x2,y2] = matrixTo1D(self.checkpoints);
            [x1,y1,x2,y2] = removeLastFromMatrix(x1,y1,x2,y2);
            
            load hospital;
            X = [hospital.Age hospital.Weight];
            Y = [20 162; 30 169; 40 168; 50 170; 60 171];   % New patients
            
            Idx = knnsearch(X,Y)
            
            X = [x1',y1'];
            Y = [x2',y2'];
            idx = knnsearch(X,Y);
            self.checkpoints = [x1(idx);y1(idx);x2;y2];
            self.checkpoints
        end
    end
end
