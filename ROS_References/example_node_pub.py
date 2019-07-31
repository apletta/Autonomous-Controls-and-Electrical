#! /usr/bin/env python # makes sure script will be executed as python

import rospy # necessary to use python with ROS

# Define message
from std_msgs.msg import String # allows for reusing String message type for publishing
# # OR
# msg = String() # set msg type
# msg.data = str # initialize fields
# # OR
# String(data=str) # one step

def talker(): # method defining what node will publish
	pub = rospy.Publisher('chatter', String, queue_size=10) # defines what topic node will publish to (chatter), message type (String, of class std_msgs.msg.String), and amount of queued messages to hold if any subscriber(s) is not taking them fast enough
	rospy.init_node('talker', anonymous=True) # defines name of node (talker) - name cannot have any slashes, anonymous=True adds random numbers to the end of the name to make node unique so nodes with the same name could be used
	rate = rospy.Rate(10) # sets looping rate for while loop
	while not rospy.is_shutdown(): # checking node is not shutdown
		hello_str = "hello world %s" % rospy.get_time()
		rospy.loginfo(hello_str) # prints messages to screen, writes messages to node's log file, writes messages to rosout.rosout for debugging
		pub.publish(hello_str) # publishes string to topic (chatter)
		rate.sleep() # pauses to maintain set loop rate

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException: # catch node shutdown (ctrl-c)
		pass
