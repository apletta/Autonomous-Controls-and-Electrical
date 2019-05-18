% Adds initial point of the specified arrays to the end of the array. Used
% to create closed looped data
function [varargout] = addInitialPoint(varargin)

for i = 1:length(varargin)
    
    mat = varargin{i};
    
    s = size(mat);

    % Determines which direction matrix is shaped
    if s(1) < s(2)
        mat(:,end+1) = mat(:,1);
        varargout{i} = mat;
    else
        mat(end+1,:) = mat(1,:);
        varargout{i} = mat;
    end
end