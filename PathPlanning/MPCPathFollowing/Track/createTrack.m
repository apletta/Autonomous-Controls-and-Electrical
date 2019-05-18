% Track creator for testing purposes
% Displays a figure and allows user to click and describe a path
% When key 'q' is pressed, figure is exited and the files are saved
% Resulting values will be saved to a mat file
function createTrack()

figure
hold on

ylim([0,100]);
xlim([0,100]);

x = [];
y = [];

while true
    
    % Records coordinate and buttons when user action is recieved
    [xp,yp,button] = ginput(1);
    
    % If 'q' key is pressed
    if button == 113 
        close all
        break;
    end
    
    x(end+1,:) = xp;
    y(end+1,:) = yp;
    plot(x,y,'^k', ...
        'MarkerSize',5);
end

% Save data to mat file format
disp('Saving data...')
save data/testTrack x y
disp('Data saved.')