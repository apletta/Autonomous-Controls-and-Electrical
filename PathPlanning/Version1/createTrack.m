% Track creator for testing purposes
% Displays a figure and waits for user to input a set of blue cones
% When key 'q' is pressed, the cones inputed are now yellow cones
% Resulting values will be saved to a csv file
function createTrack()

figure
hold on

ylim([0,50]);
xlim([0,50]);

blue = [];
yellow = [];
qpressed = false;

while true
    
    % Records coordinate and buttons when user action is recieved
    [x,y,button] = ginput(1);
    
    % If 'q' key is pressed
    if button == 113 
        if ~qpressed
            qpressed = true;
            continue;
        end
        break;
    end
    
    if qpressed
        yellow(end+1,:) = [x;y];
        plot(x,y,'^k', ...
            'MarkerSize',5, ...
            'MarkerFaceColor','y');
    else
        blue(end+1,:) = [x;y];
        plot(x,y,'^k', ...
            'MarkerSize',5, ...
            'MarkerFaceColor','b');
    end
end

% Save data to csv
csvwrite('Track/data/blue.csv',blue);
csvwrite('Track/data/yellow.csv',yellow);