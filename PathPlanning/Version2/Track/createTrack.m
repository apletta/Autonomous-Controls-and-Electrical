% Track creator for testing purposes
% Displays a figure and waits for user to input a set of blue cones
% When key 'q' is pressed, the cones inputed are now yellow cones
% Resulting values will be saved to a csv file
function createTrack()

figure
hold on

ylim([0,100]);
xlim([0,100]);

points = [];

while true
    
    % Records coordinate and buttons when user action is recieved
    [x,y,button] = ginput(1);
    
    % If 'q' key is pressed
    if button == 113 
        break;
    end
    
    points(end+1,:) = [x;y];
    plot(x,y,'^k', ...
        'MarkerSize',5);
end

% Save data to csv
csvwrite('Data/TrackData.csv',[points,repmat(3,1,length(points))']);