function [L,R,k] = generateArcParam(track)
    % Radius of curvature and curvature vector for 2D or 3D curve
    %  [L,R,Kappa] = curvature(X)
    %   X:   2 or 3 column array of x, y (and possibly z) coordiates
    %   L:   Cumulative arc length
    %   R:   Radius of curvature
    %   k:   Curvature vector
    
    N = track.len;
    points = [track.xy',zeros(N,1)];  % Do all calculations in 3D
    L = zeros(N,1);
    R = NaN(N,1);
    k = NaN(N,3);
    for i = 2:N-1
        [R(i),~,k(i,:)] = circumcenter(points(i,:)',points(i-1,:)',points(i+1,:)');
        L(i) = L(i-1)+norm(points(i,:)-points(i-1,:));
    end
    i = N;
    L(i) = L(i-1)+norm(points(i,:)-points(i-1,:));
    k = k(:,1:2);
    R(isnan(R)) = Inf;
    
    function [R,M,k] = circumcenter(A,B,C)
        % Center and radius of the circumscribed circle for the triangle ABC
        %  A,B,C  3D coordinate vectors for the triangle corners
        %  R      Radius
        %  M      3D coordinate vector for the center
        %  k      Vector of length 1/R in the direction from A towards M
        %         (Curvature vector)
        D = cross(B-A,C-A);
        b = norm(A-C);
        c = norm(A-B);
        if nargout == 1
            a = norm(B-C);     % slightly faster if only R is required
            R = a*b*c/2/norm(D);
            return
        end
        E = cross(D,B-A);
        F = cross(D,C-A);
        G = (b^2*E-c^2*F)/norm(D)^2/2;
        M = A + G;
        R = norm(G);  % Radius of curvature
        if R == 0
            k = G;
        else
            k = G'/R^2;   % Curvature vector
        end
    end
end