function isLoopClosed = isLoopClosed(track, state,varargin)
    if ~isempty(varargin)
        error = varargin{1};
    else
        error = .5;
    end
    if sum(abs(state(1:2,end) - track.xy(:,1))) < error
        isLoopClosed = true;
    else
        isLoopClosed = false;
    end