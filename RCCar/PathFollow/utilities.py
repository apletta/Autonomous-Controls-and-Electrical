def map_steer(x): #maps input values of (inmin, inmax) for our understood range of angles to output values of(outmin, outmax) that are used for the ChangeDutyCycle
    outmax = float(5)
    outmin = float(10)
    inmax = float(30)
    inmin = float(-30)
    A = float(outmax-outmin)
    B = float(inmax - inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)

def map_motor(x):
    outmax = float(8)
    outmin = float(7.5)
    inmax = float(1)
    inmin = float(0)
    A = float(outmax-outmin)
    B = float(inmax-inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)

def steer_to(theta):
    if theta>=-30 and theta <=30:
        pass# steerPin.ChangeDutyCycle(steerMap(theta))
    else:
        print("That angle isn't in range")
    
def motor_to(rev):
    if rev>0 and rev<=1000:
        pass #motorPin.ChangeDutyCycle(motorMap(rev))
    elif rev == 0:
        pass # motorPin.ChangeDutyCycle(5)
    else:
        print("That speed isn't in range")

