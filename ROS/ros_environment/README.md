# ROS Environment Set up

This directory is intended to help explain how the ROS environment and and typical workspace is set up to provide a standard for keeping your ROS environment and workspace organized. There is also lots of support in the [first tutorials of the ROS wiki](http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment). 

Generally, you will have:
1. ROS environment
    * This should be in your system files from when you first installed ROS. To activate a certain ROS distribution, you need to source it. A typical filepath for this is:
    
    `$ source /opt/ros/<distro>/setup.bash`

2. Workspace
   * This should be in your home files and you will need to make it manually. You should name it "catkin_ws".
   
   `$ mkdir -p ~/catkin_ws/src`
   
   This will make a workspace with a src file. We make the src file so that we can use catkin_make to build it. If you check the workspace right now you will only see the src folder. Move back to the top of the workspace and running catkin_make.
   
   `$ cd ~/catkin_ws`
   
   `$ catkin_make`
   
   You will now see build and devel directories in addition to your original src directory, as well as other setup files. These files can be used to configure your workspace later. Generally, the directories should be used for :
   
   * build = where cmake and make are called to configure and build your packages
   * devel = where executables and libraries go before you install your packages
   * src = where active packages you want to use go

If you're ever unsur of where your ROS distribution and workspace are located, you can check the path using the following command:

    `$ echo $ROS_PACKAGE_PATH`
    
and you should get something like:

    `/home/youruser/catkin_ws/src:/opt/ros/kinetic/share`
    
The colon separates the path to your workspace and active ROS distribution.
