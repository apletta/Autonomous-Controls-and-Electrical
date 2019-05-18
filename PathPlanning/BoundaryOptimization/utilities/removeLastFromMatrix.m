% Removes last values of the specified matrices.
function [varargout] = removeLastFromMatrix(varargin)

for i = 1:length(varargin)
    
    mat = varargin{i};
    
    s = size(mat);

    % Determines size of matrix
    if s(1) < s(2)
        varargout{i} = mat(:,1:end-1);
    else
        varargout{i} = mat(1:end-1,:);
    end
end