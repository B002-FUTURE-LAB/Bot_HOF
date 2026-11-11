[ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False
export CYCLONEDDS_URI="/etc/turtlebot4/cyclonedds_rpi.xml"
export FASTRTPS_DEFAULT_PROFILES_FILE="/etc/turtlebot4/fastdds_rpi.xml"
export ROBOT_NAMESPACE=""
export ROS_DOMAIN_ID="0"
export ROS_DISCOVERY_SERVER="127.0.0.1:11811;192.168.0.129:11811;"
export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"
export TURTLEBOT4_DIAGNOSTICS="1"
export WORKSPACE_SETUP="/opt/ros/jazzy/setup.bash"
export ROBOT_SETUP=/etc/turtlebot4/setup.bash

source $WORKSPACE_SETUP
