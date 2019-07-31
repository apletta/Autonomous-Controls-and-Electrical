import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## --> Initial state x_0, starting x, y, x_dot, y_dot
x = np.matrix([[0.0, 0.0, 0.0, 0.0]]).T

#print(x, x.shape)
#plt.scatter(float(x[0]),float(x[1]), s=100)
#plt.title('Initial Location')
#plt.show()


## --> Initial uncertainty P_0, make relatively large to start
P = np.diag([1000.0, 1000.0, 1000.0, 1000.0])
#print(P, P.shape)

# plot of covariance matrix P
# fig = plt.figure(figsize=(6, 6)) 
# im = plt.imshow(P, interpolation="none", cmap=plt.get_cmap('binary'))
# plt.title('Initial Covariance Matrix $P$')
# ylocs, ylabels = plt.yticks()
# # set the locations of the yticks
# plt.yticks(np.arange(7))
# # set the locations and labels of the yticks
# plt.yticks(np.arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$'), fontsize=22)

# xlocs, xlabels = plt.xticks()
# # set the locations of the yticks
# plt.xticks(np.arange(7))
# # set the locations and labels of the yticks
# plt.xticks(np.arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$'), fontsize=22)

# plt.xlim([-0.5,3.5])
# plt.ylim([3.5, -0.5])

# from mpl_toolkits.axes_grid1 import make_axes_locatable
# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "5%", pad="3%")
# plt.colorbar(im, cax=cax);

#plt.show()


## --> Dynamic matrix A, from motion profile
dt = 0.1 # time step between filter cycles

A = np.matrix([[1.0, 0.0, dt, 0.0],
              [0.0, 1.0, 0.0, dt],
              [0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 1.0]])
#print(A, A.shape)


## --> Measurement matrix H, transforms measurements to motion space
H = np.matrix([[0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 1.0]])
#print(H, H.shape)


## --> Measurement noise covariance, noise in sensors
ra = 10.0**2 # noise

R = np.matrix([[ra, 0.0],
              [0.0, ra]])
#print(R, R.shape)


# View distributions of R, Plot between -10 and 10 with .001 steps.
# xpdf = np.arange(-10, 10, 0.001)
# plt.subplot(121)
# plt.plot(xpdf, norm.pdf(xpdf,0,R[0,0]))
# plt.title('$\dot x$')

# plt.subplot(122)
# plt.plot(xpdf, norm.pdf(xpdf,0,R[1,1]))
# plt.title('$\dot y$')
# plt.tight_layout()
#plt.show()


## --> Process noise covariance Q, noise in model
sv = 8.8

G = np.matrix([[0.5*dt**2],
               [0.5*dt**2],
               [dt],
               [dt]])

Q = G*G.T*sv**2

from sympy import Symbol, Matrix
from sympy.interactive import printing
printing.init_printing()
dts = Symbol('dt')
Qs = Matrix([[0.5*dts**2],[0.5*dts**2],[dts],[dts]])

Qs*Qs.T

# plot covariance matrix Q
# fig = plt.figure(figsize=(6, 6))
# im = plt.imshow(Q, interpolation="none", cmap=plt.get_cmap('binary'))
# plt.title('Process Noise Covariance Matrix $Q$')
# ylocs, ylabels = plt.yticks()
# # set the locations of the yticks
# plt.yticks(np.arange(7))
# # set the locations and labels of the yticks
# plt.yticks(np.arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$'), fontsize=22)

# xlocs, xlabels = plt.xticks()
# # set the locations of the yticks
# plt.xticks(np.arange(7))
# # set the locations and labels of the yticks
# plt.xticks(np.arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$'), fontsize=22)

# plt.xlim([-0.5,3.5])
# plt.ylim([3.5, -0.5])

# from mpl_toolkits.axes_grid1 import make_axes_locatable
# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "5%", pad="3%")
# plt.colorbar(im, cax=cax);

# plt.show()


## --> Initialize identity matrix I
I = np.eye(4)
#print(I, I.shape)


## --> Generate random measurements
m = 200 # Measurements
vx= 20 # in X
vy= 10 # in Y

mx = np.array(vx+np.random.randn(m))
my = np.array(vy+np.random.randn(m))

measurements = np.vstack((mx,my))

# print(measurements.shape)
# print('Standard Deviation of Acceleration Measurements=%.2f' % np.std(mx))
# print('You assumed %.2f in R.' % R[0,0])

# --> plot randomly generated measurements
fig = plt.figure(figsize=(16,5))

plt.step(range(m),mx, label='$\dot x$')
plt.step(range(m),my, label='$\dot y$')
plt.ylabel(r'Velocity $m/s$')
plt.title('Measurements')
plt.legend(loc='best',prop={'size':18})

plt.show()


## --> Plotting
# Preallocation for Plotting
xt = []
yt = []
dxt= []
dyt= []
Zx = []
Zy = []
Px = []
Py = []
Pdx= []
Pdy= []
Rdx= []
Rdy= []
Kx = []
Ky = []
Kdx= []
Kdy= []

def savestates(x, Z, P, R, K):
    xt.append(float(x[0]))
    yt.append(float(x[1]))
    dxt.append(float(x[2]))
    dyt.append(float(x[3]))
    Zx.append(float(Z[0]))
    Zy.append(float(Z[1]))
    Px.append(float(P[0,0]))
    Py.append(float(P[1,1]))
    Pdx.append(float(P[2,2]))
    Pdy.append(float(P[3,3]))
    Rdx.append(float(R[0,0]))
    Rdy.append(float(R[1,1]))
    Kx.append(float(K[0,0]))
    Ky.append(float(K[1,0]))
    Kdx.append(float(K[2,0]))
    Kdy.append(float(K[3,0]))


## --> Predict and update cycle, loop through for all measurements
def KF(x,A,P,Q,R):
	for n in range(len(measurements[0])):
	 
	    # Time Update (Prediction)
	    # ========================
	    # Project the state ahead
	    x = A*x
	    
	    # Project the error covariance ahead
	    P = A*P*A.T + Q
	    
	    
	    # Measurement Update (Correction)
	    # ===============================
	    # Compute the Kalman Gain
	    S = H*P*H.T + R
	    K = (P*H.T) * np.linalg.pinv(S)

	    
	    # Update the estimate via z
	    Z = measurements[:,n].reshape(2,1)
	    y = Z - (H*x)                            # Innovation or Residual
	    x = x + (K*y)
	    
	    # Update the error covariance
	    P = (I - (K*H))*P
	    


	    # Save states (for Plotting)
	    savestates(x, Z, P, R, K)


## --> Helper function for plotting kalman gains
def plot_K():
    fig = plt.figure(figsize=(8,4))
    plt.plot(range(len(measurements[0])),Kx, label='Kalman Gain for $x$')
    plt.plot(range(len(measurements[0])),Ky, label='Kalman Gain for $y$')
    plt.plot(range(len(measurements[0])),Kdx, label='Kalman Gain for $\dot x$')
    plt.plot(range(len(measurements[0])),Kdy, label='Kalman Gain for $\dot y$')

    plt.xlabel('Filter Step')
    plt.ylabel('')
    plt.title('Kalman Gain (the lower, the more the measurement matches the prediction)')
    plt.legend(loc='best',prop={'size':22})
    
    plt.show()

## --> Helper function for plotting uncertainty P
def plot_P():
    fig = plt.figure(figsize=(8,4))
    plt.plot(range(len(measurements[0])),Px, label='$x$')
    plt.plot(range(len(measurements[0])),Py, label='$y$')
    plt.plot(range(len(measurements[0])),Pdx, label='$\dot x$')
    plt.plot(range(len(measurements[0])),Pdy, label='$\dot y$')

    plt.xlabel('Filter Step')
    plt.ylabel('')
    plt.title('Uncertainty (Elements from Matrix $P$)')
    plt.legend(loc='best',prop={'size':22})

    plt.show()

## --> Helper function for plotting state estimates
def plot_x():
    fig = plt.figure(figsize=(8,4))
    plt.step(range(len(measurements[0])),dxt, label='$\dot x$')
    plt.step(range(len(measurements[0])),dyt, label='$\dot y$')

    plt.axhline(vx, color='#999999', label='$\dot x_{real}$')
    plt.axhline(vy, color='#999999', label='$\dot y_{real}$')

    plt.xlabel('Filter Step')
    plt.title('Estimate (Elements from State Vector $x$)')
    plt.legend(loc='best',prop={'size':22})
    plt.ylim([0, 30])
    plt.ylabel('Velocity')

    plt.show()


## --> Helper function for plotting position
def plot_xy():
    fig = plt.figure(figsize=(8,4))
    plt.scatter(xt,yt, s=20, label='State', c='k')
    plt.scatter(xt[0],yt[0], s=100, label='Start', c='g')
    plt.scatter(xt[-1],yt[-1], s=100, label='Goal', c='r')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Position')
    plt.legend(loc='best')
    plt.axis('equal')

    plt.show()


KF(x,A,P,Q,R) # run kalman filter 
# x = state 
# A = dynamic equations
# P = uncertainty in state variables
# Q = noise inherent to system
# R = noise in measurements

plot_K() # plot kalman gains
plot_P() # plot uncertainty
plot_x() # plot state estimates
plot_xy() # plot x and y position








