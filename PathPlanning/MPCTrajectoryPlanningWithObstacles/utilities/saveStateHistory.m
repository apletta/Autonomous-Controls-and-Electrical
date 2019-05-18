function saveStateHistory(stateHistory)
    
    disp('rtest')
    
    stateHistory = round(stateHistory',2);
    stateHistory(stateHistory == -0) = 0;
    
    headers = 'x,y,vx,vy';
    
    fileName = '../../RCCar/PredefinedPath/data/CCWCircle.csv';
    
    csvwrite(fileName,stateHistory)

    S = fileread(fileName);
    S = [headers, char(10), S];
    FID = fopen(fileName, 'w');
    if FID == -1, error('Cannot open file %s', fileName); end
    fwrite(FID, S, 'char');
    fclose(FID);