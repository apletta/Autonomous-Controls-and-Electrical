classdef Car
    
    properties
        state
        transform
    end
    
    methods
        function self = Car(initState)
            self.state = initState;
            
            %initTransform(self);
        end
    end
end

