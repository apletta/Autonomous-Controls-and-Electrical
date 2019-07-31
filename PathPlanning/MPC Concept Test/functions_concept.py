import numpy as np
import itertools
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from timeit import default_timer as timer


def gen_sequence_phi(numToGenerate, maxInput):
    step = 2*maxInput/(numToGenerate-1)
    sequence = np.zeros(numToGenerate)
    new = -maxInput
    for i in range(numToGenerate):
        sequence[i] = new
        new = new + step
    return sequence 

def gen_sequence_a(numToGenerate, maxThrottle, maxBrake):
    a_sequence = [maxBrake]
    return np.append(a_sequence, np.linspace(0, maxThrottle, numToGenerate-1))

def gen_v_thresh(numToGenerate, minThresh, maxThresh):
    return np.linspace(minThresh, maxThresh, numToGenerate)

def find_obstacles_in_range(obstacles, current_position, v_max, a_maxThrottle, a_maxBrake, dt, H_p):
    obstacles_in_range = []

    a = max(abs(a_maxThrottle), abs(a_maxBrake))
    r_max = 0

    for i in range(H_p):
        # r_max = r_max + v_max*dt + 0.5*a_maxThrottle*(dt**2) # use for general case
        r_max = r_max + v_max*dt # use if certain won't go over v_max

    for obstacle in obstacles:
        obstacle_distance = math.sqrt( (obstacle[0]-current_position[0])**2 +(obstacle[1]-current_position[1])**2 )
        if obstacle_distance <= r_max:
            obstacles_in_range.append(obstacle)

    return obstacles_in_range, r_max

def find_lines_in_range(lines, lines_buffered, current_position, v_max, a_maxThrottle, a_maxBrake, dt, H_p):
    lines_in_range = []

    a = max(abs(a_maxThrottle), abs(a_maxBrake))
    r_max = 0

    for i in range(H_p):
        # r_max = r_max + v_max*dt + 0.5*a_maxThrottle*(dt**2) # use for general case
        r_max = r_max + v_max*dt # use if certain won't go over v_max

    for newLine in lines:
        line_dist = dist_to_line(newLine[0][0], newLine[0][1], newLine[1][0], newLine[1][1], current_position[0], current_position[1])
        if line_dist <= r_max:
            lines_in_range.append(newLine)

    for packed_line in lines_buffered:
        for newLine in packed_line:
            line_dist = dist_to_line(newLine[0][0], newLine[0][1], newLine[1][0], newLine[1][1], current_position[0], current_position[1])
            if line_dist <= r_max:
                lines_in_range.append(newLine)

    return lines_in_range, r_max

# https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
def dist_to_line(x1, y1, x2, y2, x3, y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = (dx*dx + dy*dy)**.5

    return dist

def buffer_for_line(line, line_buffer):
    # read in line
    x1_left = min(line[0][0], line[1][0]) 
    x1_right = max(line[0][0], line[1][0])

    if x1_left == line[0][0]: # first point is left point
        y1_left = line[0][1]
        y1_right = line[1][1]
    else: # second point should be left point
        y1_left = line[1][1]
        y1_right = line[0][1]

    # find intermediate angles and points

    diff_x = x1_left-x1_right

    if diff_x != 0: # slope defined (non-vertical)

        theta = math.atan( (y1_left-y1_right)/(diff_x) )

        if theta < 0: # slope is negative
            theta = -theta

            # intermediary/projected points
            x_inter_left = x1_left - line_buffer*math.cos(theta)
            y_inter_left = y1_left + line_buffer*math.sin(theta)

            x_inter_right = x1_right + line_buffer*math.cos(theta)
            y_inter_right = y1_right - line_buffer*math.sin(theta)

            # find end points of buffer line segments
            x1 = x_inter_left - line_buffer*math.sin(theta)
            y1 = y_inter_left - line_buffer*math.cos(theta)

            x2 = x_inter_left + line_buffer*math.sin(theta)
            y2 = y_inter_left + line_buffer*math.cos(theta)

            x3 = x_inter_right + line_buffer*math.sin(theta)
            y3 = y_inter_right + line_buffer*math.cos(theta)

            x4 = x_inter_right - line_buffer*math.sin(theta)
            y4 = y_inter_right - line_buffer*math.cos(theta)

        else: # slope is positive

            # intermediary/projected points
            x_inter_left = x1_left - line_buffer*math.cos(theta)
            y_inter_left = y1_left - line_buffer*math.sin(theta)

            x_inter_right = x1_right + line_buffer*math.cos(theta)
            y_inter_right = y1_right + line_buffer*math.sin(theta)

            # find end points of buffer line segments
            x1 = x_inter_left + line_buffer*math.sin(theta)
            y1 = y_inter_left - line_buffer*math.cos(theta)

            x2 = x_inter_left - line_buffer*math.sin(theta)
            y2 = y_inter_left + line_buffer*math.cos(theta)

            x3 = x_inter_right - line_buffer*math.sin(theta)
            y3 = y_inter_right + line_buffer*math.cos(theta)

            x4 = x_inter_right + line_buffer*math.sin(theta)
            y4 = y_inter_right - line_buffer*math.cos(theta)

    else: # slope is undefined (vertical)

        x = line[0][0] # can use either x value because they are the same
        y_top = max(line[0][1], line[1][1])
        y_bot = min(line[0][1], line[1][1])

        # intermediary/projected points
        y_inter_top = y_top + line_buffer
        y_inter_bot = y_bot - line_buffer

        # find end points of buffer line segments
        x1 = x - line_buffer
        y1 = y_inter_top

        x2 = x + line_buffer
        y2 = y_inter_top

        x3 = x + line_buffer
        y3 = y_inter_bot

        x4 = x - line_buffer
        y4 = y_inter_bot

    # collect all four new line segments
    buffer_lines = [ [[x1, y1],[x2, y2]], [[x2, y2],[x3, y3]], [[x3, y3],[x4, y4]], [[x4, y4],[x1, y1]] ]

    return buffer_lines




def orientation(a, b, c):
    # a and b end points of a segment, c point to check
    
    #slope1 = (b[2]-a[2])/(b[1]-a[1])
    #slope2 = (c[2]-b[2])/(c[1]-b[1])
    #val = slope1 - slope2
    
    val = (b[1]-a[1])*(c[0]-b[0]) - (c[1]-b[1])*(b[0]-a[0])
    
    if(val<0):
        return 1 # clockwise
    
    if(val>0):
        return 2 # counterclockwise 

    return 0 # slopes the same

def point_on_segment(a, b, c):
    # a and b end points of a segment, c point to check
    # only gets called if c is determined by orientation(a,b,c) to be collinear with ab
    # returns true if c on segment ab, false otherwise 
    if ( min(a[0], b[0]) <= c[0] and c[0] <= max(a[1], b[1]) ):
        if ( min(a[1], b[1]) <= c[1] and c[1] <= max(a[1], b[1]) ):
            return True

    return False


def intersection(a, b, c, d):
    # a and b existing segment, c and d segment to check
    # returns true if intersection discovered, false otherwise
    
    # ab vs new segment test
    ab_vs_c = orientation(a,b,c)
    ab_vs_d = orientation(a,b,d)
    
    # new segment vs ab test
    cd_vs_a = orientation(c,d,a)
    cd_vs_b = orientation(c,d,b)
    
    # if both orientation tests are different, then segments cross 
    if(ab_vs_c != ab_vs_d and cd_vs_a != cd_vs_b):
        return True
    
    # verify any collinearity does not result in crossing
    
    # c collinear with ab
    if(ab_vs_c == 0 and point_on_segment(a,b,c)):
        return True
    
    # d collinear with ab
    if(ab_vs_d == 0 and point_on_segment(a,b,d)):
        return True
    
    # a collinear with cd
    if(cd_vs_a == 0 and point_on_segment(c,d,a)):
        return True
    
    # b collinear with cd
    if(cd_vs_b == 0 and point_on_segment(c,d,b)):
        return True
    
    # if crossing not detected, return false
    return False   


def calc_score(control, dt, H_p, x, y, a, v_max, v_min, current_v, current_heading, k, goal, obstacles, lines_in_range, avoidance_radius, previousLoc_radius, robot_memory, detection_radius):
    W_a = 1                 # generally leave at one if don't mind changes in velocity that much
    W_phi = 1e3               # increase to tune amount of turning, higher good to prevent going in circles (continuing to turn) but need low enough to have flexible route
    W_dist = 2e1              # can be somewhat low because sum_dist already relatively large
    W_obs = 1               # leave at 1, cost_obs applies weight
    cost_obs = 2e10         # only gets applied if within obstacle zone
    W_lineCross = 1         # leave at 1, cost_lineCross applies weight
    cost_lineCross = 1e10   # applied whenever path would cross over line obstacle
    W_vmin = 1              # leave at 1, cost_vmin applies weight
    cost_vmin = 1e3           # only gets applied if velocity below certain threshold
    W_vmax = 1              # leave at 1, cost_vmax applies weight
    cost_vmax = 1e6         # cost whenever velocity goes over max velocity, keep high to prevent from going too fast
    W_reverse = 1           # leave at 1, cost_reverse applies weight
    cost_reverse = 1e2        # keep velocity from going negative
    W_fast = 1e1              # increase to make robot want to keep speed closer to max velocity
    W_previousLoc = 1       # leave at 1, cost_previousLoc applies weight
    cost_previousLoc = 1e5  # applied whenever path would be within previousLoc_radius of a point in the robot_memory (not the full path, just a certain number of points back)
    

    # fast velocity
    sum_fast = 0
    for i in range(H_p):
        new_v = calc_v(current_v, control[i][0], dt)
        sum_fast = sum_fast + (new_v - v_max)**2
    J_fast = W_fast*sum_fast

    # acceleration
    sum_a = 0 # initialize with difference in first applied move from current state
    for i in range(H_p):
        sum_a = sum_a + (control[i][0])**2 # sum all acceleration inputs
    J_a = W_a*sum_a
    
    # steer angle change, want to minimize entirely to limit steering change
    sum_phi = 0 # initialize with difference in first applied move from current state
    for i in range(H_p):
        sum_phi = sum_phi + (control[i][1]/360)**2 # divide by 360 to put on sum on similar scale as other weights
    J_phi = W_phi*sum_phi

    # distance to goal, distance to obstacles, backtrack prevention
    sum_dist = 0
    sum_obs = 0
    sum_vmin = 0  # costly to return to same position, want to keep exploring if speed below vmin (aka stuck)
    sum_reverse = 0
    sum_previousLoc = 0
    sum_vmax = 0
    sum_lineCross = 0
    x_control = x.copy()
    y_control = y.copy()


    new_heading = current_heading 
    new_v = current_v

    for i in range(len(control)):

        new_heading = calc_heading(new_heading, control[i][1]) # new intial future heading, current heading + next steering command
        x2, y2 = calc_position(x_control[k+i], y_control[k+i], new_v, control[i][0], dt, new_heading)
        new_v = calc_v(new_v, control[i][0], dt) # new initial future velocity 
       
        # check distance to goal
        sum_dist = sum_dist + math.sqrt( (x2-goal[0])**2 + (y2-goal[1])**2 )

        # check distance to all obstacles
        for j in range(len(obstacles)):
            clearance = math.sqrt( (x2-obstacles[j][0])**2 + (y2-obstacles[j][1])**2 )

            if clearance <= avoidance_radius:
                sum_obs = sum_obs + cost_obs

        # check if crossing any lines
        for line in lines_in_range:
            pos1 = [x_control[k+i], y_control[k+i]]
            pos2 = [x2, y2]
            if intersection(line[0],line[1],pos1,pos2):
                sum_lineCross = sum_lineCross + cost_lineCross

        # keep robot moving within desired velocity range
        if abs(new_v) < v_min:
            sum_vmin = sum_vmin + cost_vmin
        if new_v > v_max:
            sum_vmax = sum_vmax + cost_vmax
        if new_v < 0:
            sum_reverse = sum_reverse + cost_reverse

        # check previous path
        memory_length = robot_memory
        path_length = len(x_control)    
        if path_length < robot_memory:
            memory_length = path_length

        for j in range(path_length-memory_length, path_length-5):
            dist_previousLoc = math.sqrt( (x2-x_control[j])**2 +(y2-y_control[j])**2 )
            if dist_previousLoc <= previousLoc_radius:
                sum_previousLoc = sum_previousLoc + cost_previousLoc


        # update arrays for prediction horizon steps
        x_control.append(x2)
        y_control.append(y2)




    J_dist = W_dist*sum_dist
    J_obs = W_obs*sum_obs
    J_lineCross = W_lineCross*sum_lineCross
    J_vmin = W_vmin*sum_vmin
    J_previousLoc = W_previousLoc*sum_previousLoc
    J_vmax = W_vmax*sum_vmax
    J_reverse = W_reverse*sum_reverse


    objective = J_a + J_phi + J_dist + J_obs + J_lineCross + J_vmin + J_vmax + J_reverse + J_fast + J_previousLoc 

    return J_a, J_phi, J_dist, J_obs, J_lineCross, J_vmin, J_vmax, J_reverse, J_fast, J_previousLoc


def calc_position(x1, y1, v, a, dt, phi):

    x2 = x1 + v*dt*math.sin(math.radians(phi)) + 0.5*a*(dt**2)*math.sin(math.radians(phi))
    y2 = y1 + v*dt*math.cos(math.radians(phi)) + 0.5*a*(dt**2)*math.cos(math.radians(phi))

    return x2, y2

def calc_vector_location(x1, y1, v, dt, phi):

    x2 = x1 + v*dt*math.sin(math.radians(phi))
    y2 = y1 + v*dt*math.cos(math.radians(phi)) 

    return x2, y2

def calc_heading(current_heading, new_phi):
    return current_heading + new_phi

def calc_v(current_v, new_a, dt):
    return current_v + new_a*dt


def goalCheck(x, y, goal, goalThresh):
    distance = math.sqrt( (x[-1]-goal[0])**2 + (y[-1]-goal[1])**2 )
    if distance < goalThresh:
        return True
    else:
        return False

def plotPath(robot_dim, robot_memory, scan_zone, x, y, dt, current_heading, goal, goalThresh, waypoints, wayPointThresh, obstacles, obstacle_radius, lines, lines_buffered, avoidance_radius, optimal_plot, active_plot):

    fig, ax = plt.subplots()

    new_obstacle = []

    def onclick(event):
        if event.xdata != None and event.ydata != None:
            new_obstacle.append([event.xdata, event.ydata])

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # plot path and goal
    path_length = len(x)    
    if path_length < robot_memory:
        robot_memory = path_length
    plt.plot(x[path_length-robot_memory:], y[path_length-robot_memory:], marker=".")

    plt.scatter(goal[0], goal[1], color="green")
    goal_circle = plt.Circle((goal[0], goal[1]), goalThresh, alpha=0.2, color='green')
    ax.add_artist(goal_circle)

    for waypoint in waypoints:
        plt.scatter(waypoint[0], waypoint[1], alpha=0.4, color="green")
        waypoint_circle = plt.Circle((waypoint[0], waypoint[1]), wayPointThresh, alpha=0.1, color='green')
        ax.add_artist(waypoint_circle)

    # plot robot body
    robot_length = robot_dim[0]
    robot_width = robot_dim[1]
    rect_phi = 90 - current_heading

    x_rear, y_rear = calc_vector_location(x[-1], y[-1], -robot_length/2, 1, current_heading)
    x_front, y_front = calc_vector_location(x[-1], y[-1], robot_length/2, 1, current_heading)
    rect_x = x_rear+(robot_width/2)*math.sin(math.radians(rect_phi))
    rect_y = y_rear-(robot_width/2)*math.cos(math.radians(rect_phi))

    plt.scatter(x_front, y_front, color="blue", marker="*")
    rect = patches.Rectangle((rect_x, rect_y), robot_length, robot_width, rect_phi, linewidth=1, edgecolor='blue',facecolor='none')
    ax.add_patch(rect)

    scan_circle = plt.Circle((x[-1], y[-1]), scan_zone, alpha=0.1, color='blue')
    ax.add_artist(scan_circle)


    # plot obstacles
    for center in obstacles: # circular obstacles
        obstacle_circle = plt.Circle((center[0], center[1]), obstacle_radius, color='red')
        avoidance_circle = plt.Circle((center[0], center[1]), avoidance_radius, alpha=0.2, color='red')
        ax = plt.gca()
        ax.add_artist(obstacle_circle)
        ax.add_artist(avoidance_circle)

    # plot lines
    for line in lines: 
        line_x = [line[0][0], line[1][0]]
        line_y = [line[0][1], line[1][1]]
        plt.plot(line_x, line_y, color="red")

    # plot line buffers
    for buffer_lines in lines_buffered:
        for buffer_line in buffer_lines:
            line_x = [buffer_line[0][0], buffer_line[1][0]]
            line_y = [buffer_line[0][1], buffer_line[1][1]]
            plt.plot(line_x, line_y, color="red", alpha=0.2)
            #plt.scatter(buffer_line[0][0], buffer_line[0][1]) # plot buffer line end points

    # format plot
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("MPC Based Path Planning")
    ax.axis("square")
    border = 5

    if active_plot == 0: # go as fast as time steps allow, plot future moves
        plt.scatter(optimal_plot[0][:], optimal_plot[1][:], color="orange", marker="x")

        plt.show(block=False)
        plt.pause(0.0000001)
        plt.close()
    elif active_plot == 1: # stepwise, plot future moves
        plt.scatter(optimal_plot[0][:], optimal_plot[1][:], color="orange", marker="x")

        plt.show(block=True)
    else: # stepwise, only plot current moves
        plt.title("MPC Based Path Planning \n------->  Complete!  <-------")

        plt.show(block=True)

    return new_obstacle





