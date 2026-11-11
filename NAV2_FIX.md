# Nav2 Configuration & Troubleshooting Guide

This guide explains how to run and diagnose the customized Nav2 stack for the TurtleBot 4.

## 🔧 Key Fixes Implemented

1. **RMW Implementation**: Standardized on `rmw_fastrtps_cpp` (default in ROS 2 Jazzy and compatible with iRobot Create 3 firmware).
2. **Lifecycle & Startup Timeouts**: Added custom launch wrappers (`launch/localization_lifecycle_timeout.launch.py` and `launch/nav2_lifecycle_timeout.launch.py`) and custom parameters (`config/nav2_custom.yaml`).
3. **Diagnostic Scripts**: Tools to inspect TF frames, `/scan`, and FastDDS Discovery Server status.

## 📁 Key Files

- `config/nav2_custom.yaml` — Custom Nav2 parameters for the B002 map
- `config/rpi_turtlebot4/` — Backed-up Raspberry Pi `/etc/turtlebot4` and OAK-D (`oakd_pro.yaml`) configurations
- `launch/localization_lifecycle_timeout.launch.py` — Localization launch with extended lifecycle timeout
- `launch/nav2_lifecycle_timeout.launch.py` — Nav2 launch with extended lifecycle timeout
- `scripts/check_nav_status.sh` — Navigation diagnostic script

## 🚀 Usage (Simulation)

### Option 1: All-in-One Launch

```bash
./sim/run_lab_world.sh true true 0.0 0.0 0.0
```

Starts Gazebo Harmonic + SLAM + Nav2 + RViz with the custom parameters.

### Option 2: Step-by-Step Launch

1. **Start Simulation + SLAM only:**
   ```bash
   ./sim/run_lab_world.sh true false 0.0 0.0 0.0
   ```
2. **Verify `/scan` and TF (`odom -> base_link`):**
   ```bash
   ros2 topic list | grep -E '/scan$|/odom$|/cmd_vel$'
   ros2 run tf2_ros tf2_echo odom base_link
   ```
3. **Launch Nav2 separately:**
   ```bash
   source /opt/ros/jazzy/setup.bash
   export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
   ros2 launch turtlebot4_navigation nav2.launch.py use_sim_time:=true
   ```
