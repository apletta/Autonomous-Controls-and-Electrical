# ROS Environment Setup

This directory is intended to help explain how the ROS environment and and typical workspace is setup to provide a standard for keeping your ROS environment and workspace organized. There is also lots of support on the ROS wiki. 

Generally, you will have:
1. ROS environment
    * This should be in your system files from when you first installed ROS. To activate a certain ROS distribution, you need to source it. A typical filepath for this is:
    `$ soruce /opt/ros/<distro>/setup.bash`

To check the path, you can run
    `$ echo $ROS_PACKAGE_PATH`
and you should get something like
    `/home/youruser/catkin_ws/src:/opt/ros/kinetic/share`
The colon separates the path to your workspace and active ROS distribution.
