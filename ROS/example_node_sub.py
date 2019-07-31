#! /usr/bin/env python # makes sure script will be executed as python

# Define message
from std_msgs.msg import String # allows for reusing String message type for publishing
# # OR
# msg = String() # set msg type
# msg.data = str # initialize fields
# # OR
# String(data=str) # one step

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data) # prints messages to screen, writes messages to node's log file, writes messages to rosout.rosout for debugging

def listener(): 
	rospy.init_node('listener', anonymous=True) # defines name of node (listener) - name cannot have any slashes, anonymous=True adds random numbers to the end of the name to make node unique so nodes with the same name could be used
	rospy.Subscriber('chatter', String, callback) # defines what topic node will subscribe to (chatter), message type (String, of class std_msgs.msg.String), and first argument for new messages (callback)
	rospy.spin() # keeps node from exiting until shutdown, does not affect subscriber callback functions (unlike in roscpp)
