classdef Track
    properties
        checkpoints
        x,y
        bx,by
        yx,yy
    end
    
    methods
        function self = Track(checkpoints)
            self.checkpoints = checkpoints;
            [self.x,self.y,self.bx,self.by,self.yx,self.yy] = ...
                points2xy(checkpoints);
        end
        
        %% GETTER METHODS
        function [x,y] = getInitialPosition(self)
            x = self.x(1);
            y = self.y(1);
        end
    end
end

