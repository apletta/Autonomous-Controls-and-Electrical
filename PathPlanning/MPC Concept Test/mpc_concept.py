import numpy as np
import itertools
from functions_concept import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from timeit import default_timer as timer


#################### INPUTS ####################

# time scale
dt = 1 # seconds in one time step (length of step is v*dt so smaller dt means smaller steps, "greater resolution", with same velocity)
start = [54, 8] # beginning location at x, y 
initialHeading = 0 # heading in degrees

goal = [140, 120] # goal location
goalThresh = 5 # minimum distance to goal to be considered at goal

# checkpoints along the way to the goal, must be in order to visit (first = index 0)
waypoints = [ [78, 103], [115, 50] ] # floorplan nav
#waypoints = [[29, 55]] # u-turn
#waypoints = []
wayPointThresh = 5 # minimum distance to waypoint to be considered at waypoint

# robot dimensions
robot_length = 10
robot_width = 5
robot_dim = [robot_length, robot_width]
detection_radius = 4
robot_memory = 0

# intitial obstacles ([x_1, y_1], [x_2, y_2], ... , [x_n, y_n]), all circular
obstacles = [[100, 70], [105, 75]] # floorplan nav
#obstacles = [[78, 53],[69, 67],[63, 68],[48, 67],[40, 54], [55, 69], [73, 59], [43, 61], [71, 62]] # u-turn
#obstacles = [[70, 22],[56.5, 30]] # circle-jump
#obstacles = []
obstacle_radius = 5 # radius of actual obstacle
#min_buffer = math.sqrt( (robot_width/2)**2 + (robot_length/2)**2 ) # distance to avoid obstacle by
min_buffer = 3

lines = [ [[80, 0], [80, 90]], [[80, 120],[80, 140]], [[115, 65],[115, 140]], [[115, 35],[115, 0]], [[80, 140], [115,140]], [[80,0],[115,0]]  ] # floorplan nav
#lines = [ [[80, 120],[80, 140]] ]
#lines = []
line_buffer = 3
lines_buffered = []
for line in lines:
    lines_buffered.append(buffer_for_line(line, line_buffer))

# generate control sequences    
v_max = 4 # max velocity
v_min = 0.01 # min desired velocity
a_maxThrottle = 2 # max acceleration input
a_maxBrake = -2 # max brake/reverse input
phi_max = 40 # max steering angle in degrees

# num_phi = 3 # number of potential steering angle commands, must be odd to allow for 0deg steer
# num_a = 3 # number of potential acceleration commands, must be >=3 to allow for reverse, zero change, and at least one command to go forward
v_thresh = 0.75*v_max # cut off between slow and fast control (slow has more steering but smaller H_p, fast less steering but more H_p)

# other control
previousLoc_radius = 12


#################### SETUP/TESTING ####################

# initial control commands (v=velocity, phi=steering angle input) and state (x, y, heading)
phi = [initialHeading]
a = [0]
x = [start[0]] 
y = [start[1]]
current_heading = 0 
current_v = 0

# stop conditions
max_seconds = 120 # max simulation time in seconds
max_k = (max_seconds-dt)/dt # max number of simulation steps

run_once = False # toggle True/False to execute code once or as many times as set (see if statement for stop conditions below)

# miscellaenous
k = 0 # initialize time steps
goalReached=False # initialize flag for if at goal
avoidance_radius = obstacle_radius + min_buffer # min distance to be from center of obstacle, used for calculation/plotting
run_time = 0 # initialize track of how long program has run for as sum of execution loops

num_wayPoints = len(waypoints)
wayPointsReached = False
if num_wayPoints == 0:
    wayPointsReached = True
waypointCheck = False

# plotting switch
# 0 --> dynamic with future path
# 1 --> step-wise with future path
# 2 --> step-wise, no future path
active_plot = 1



#################### CALCULATIONS ####################

while(goalReached==False): # run until goal is reached or while loop broken for other conditions

    start = timer()

    # dynamically change prediction horizon
    if current_v < v_thresh:
        H_p = 2
        H_c = 1
        num_phi = 7
        num_a = 5
        phi_sequence = gen_sequence_phi(num_phi, phi_max) # sequence of potential steering angle input commands
        a_sequence = gen_sequence_a(num_a, a_maxThrottle, a_maxBrake)
    
    elif current_v >= v_thresh:
        H_p = 3
        H_c = 1
        num_phi = 5
        num_a = 3
        phi_sequence = gen_sequence_phi(num_phi, phi_max) # sequence of potential steering angle input commands
        a_sequence = gen_sequence_a(num_a, a_maxThrottle, a_maxBrake)
        phi_sequence = phi_sequence[1:-1] # decrease largest two commands in phi_sequence to decrease num_phi by 2, allows for larger H_p

    combos = [[a,b] for a in a_sequence for b in phi_sequence] # generate possible control inputs for any time step

    # limit obstacles to those in range of potential collision
    current_position = [x[-1], y[-1]]
    obstacles_in_range, scan_zone = find_obstacles_in_range(obstacles, current_position, v_max, a_maxThrottle, a_maxBrake, dt, H_p)
    lines_in_range, scan_zone = find_lines_in_range(lines, lines_buffered, current_position, v_max, a_maxThrottle, a_maxBrake, dt, H_p)

    print("\n================== k =",k,"=====================")
    print("_______________Control inputs_________________")
    print("Acceleration:    ", a_sequence)
    print("Steer angles:", phi_sequence)


    # 1. find distance to goal from current position
    # 2. adjust prediction horizon to be smaller if closer to goal

    # The method that prints all  
    # possible strings of length k. 
    # It is mainly a wrapper over  
    # recursive function printAllKLengthRec()
    # https://www.geeksforgeeks.org/print-all-combinations-of-given-length/ 
    def printAllKLength(set, l_seq):

        initialScore = 1e100
        optimal = [""]*l_seq
        optimal.append(initialScore) 
      
        n = len(set)  
        prefix = []
        return printAllKLengthRec(set, prefix, n, l_seq, optimal)
      
    # The main recursive method 
    # to print all possible  
    # strings of length k 
    def printAllKLengthRec(set, prefix, n, l_seq, optimal): 
        score = optimal[-1]
        best = [1e100]
        final_costs = [] 

        # Base case: k is 0, 
        # print prefix 
        if (l_seq == 0):
            if wayPointsReached == False:
                J_a, J_phi, J_dist, J_obs, J_lineCross, J_vmin, J_vmax, J_reverse, J_fast, J_previousLoc = calc_score(prefix, dt, H_p, x, y, a, v_max, v_min, current_v, current_heading, k, waypoints[-num_wayPoints], obstacles_in_range, lines_in_range, avoidance_radius, previousLoc_radius, robot_memory, detection_radius)
            else:
                J_a, J_phi, J_dist, J_obs, J_lineCross, J_vmin, J_vmax, J_reverse, J_fast, J_previousLoc = calc_score(prefix, dt, H_p, x, y, a, v_max, v_min, current_v, current_heading, k, goal, obstacles_in_range, lines_in_range, avoidance_radius, previousLoc_radius, robot_memory, detection_radius)
            newScore = J_a + J_phi + J_dist + J_obs + J_lineCross + J_vmin + J_vmax + J_reverse + J_fast + J_previousLoc 
            if newScore < score:
                better = prefix.copy()
                better.append(newScore)
                costs = [J_a, J_phi, J_dist, J_obs, J_lineCross, J_vmin, J_vmax, J_reverse, J_fast, J_previousLoc]
                return better, costs
        
        # One by one add all characters  
        # from set and recursively  
        # call for k equals to k-1 
        print("-----------")
        print(best[-1])
        for i in range(n): 

            # Next character of input added 
            newPrefix = prefix.copy()
            newPrefix.append(set[i])
              
            # k is decreased, because  
            # we have added a new character
            new, costs = printAllKLengthRec(set, newPrefix, n, l_seq - 1, optimal)
            print("")
            print(best[-1])
            print(new[-1])
            if new[-1] < best[-1]:
                best = new
                final_costs = costs


        return best, final_costs

    optimal_sequence, final_costs = printAllKLength(combos, H_p) # find control sequence with lowest score

    print("\n_______________Control selection______________")

    # display step time vs. execution time
    sim_time = k*dt + dt
    print("Sim time  =", sim_time, "s")
    execution_time = timer()-start
    run_time = run_time + execution_time
    print("run time  =", run_time ,"s", "   (execution time =", execution_time,"s )")
    if execution_time > dt: # execution must be faster than desired time step or else can't apply control in time
        print("! EXECUTION TOO SLOW !")

    print("optimal control sequence:", optimal_sequence)
    #print(final_costs)


    # plot future path
    optimal_sequence = optimal_sequence[:-1]
    x_optimal = []
    y_optimal = []
    x_curr = x[-1]
    y_curr = y[-1]
    new_heading = current_heading
    new_v = current_v
    for i in range(len(optimal_sequence)):
        new_heading = calc_heading(new_heading, optimal_sequence[i][1]) # new intial future heading, current heading + next steering command
        x2, y2 = calc_position(x_curr, y_curr, new_v, optimal_sequence[i][0], dt, new_heading)
        x_optimal.append(x2)
        y_optimal.append(y2)
        x_curr = x_optimal[-1]
        y_curr = y_optimal[-1]
        new_v = calc_v(new_v, optimal_sequence[i][0], dt) # new initial future velocity command


    optimal_plot = [x_optimal, y_optimal]

    print("_______________State__________________________")
    print("Previous velocity   =", current_v)
    print("Previous heading    =", current_heading)
    print("Previous position   =", x[-1],",", y[-1])
    

    # Apply first steps of sequence
    for i in range(H_c):

        a.append(optimal_sequence[i][0])
        phi.append(optimal_sequence[i][1])
        new_a = a[-1]
        new_phi = phi[-1]
        current_heading = calc_heading(current_heading, new_phi) # new heading angle is current heading + latest steering input
        x2, y2 = calc_position(x[k], y[k], current_v, new_a, dt, current_heading)
        x.append(x2)
        y.append(y2)
        current_v = calc_v(current_v, new_a, dt)

        k+=1

    print()
    print("Acceleration input =", a[-1])
    print("Heading input      =", phi[-1])
    print("Time step          =", dt, "s")
    print()
    print("Current velocity    =", current_v)
    print("Current heading     =", current_heading)
    print("Current position    =", x[-1],",", y[-1])
    print("==============================================\n")

    # plot path so far and read in any new obstacles to avoid
    new_obstacles = plotPath(robot_dim, robot_memory, scan_zone, x, y, dt, current_heading, goal, goalThresh, waypoints, wayPointThresh, obstacles, obstacle_radius, lines, lines_buffered, avoidance_radius, optimal_plot, active_plot)
    if len(new_obstacles)!= 0:
        obstacles.extend(new_obstacles)

    # check for waypoints until all reached, then start checking if goal is reached

    if num_wayPoints != 0:
        waypointCheck = goalCheck(x, y, waypoints[-num_wayPoints], wayPointThresh)

    if waypointCheck == True and num_wayPoints > 0:
        num_wayPoints = num_wayPoints - 1

    if num_wayPoints == 0:
        wayPointsReached = True

    if wayPointsReached == True:
        goalReached = goalCheck(x, y, goal, goalThresh) # check if position within goal threshold

    # stop conditions: check if searching complete due to reaching goal, timeout, or testing
    if(goalReached==True):
        print()
        print("Goal Reached!")
        active_plot = 2
        robot_memory = len(x)
        plotPath(robot_dim, robot_memory, scan_zone, x, y, dt, current_heading, goal, goalThresh, waypoints, wayPointThresh, obstacles, obstacle_radius, lines, lines_buffered, avoidance_radius, optimal_plot, active_plot)
        break

    if k>max_k or run_once==True: # time out or input stop conditions
        print()
        print("Done")
        break


 
