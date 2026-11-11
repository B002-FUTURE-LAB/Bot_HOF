# Quick Start — TurtleBot 4 in the Laboratory World

## Option 1: Automated Script (Recommended)

Run in a terminal:

```bash
./sim/run_lab_world.sh
```

Or with custom arguments:

```bash
# Simulation + SLAM only (without Nav2)
./sim/run_lab_world.sh true false

# With SLAM + Nav2
./sim/run_lab_world.sh true true

# With custom initial pose (x=-1.0, y=0.0, yaw=1.57)
./sim/run_lab_world.sh true true -1.0 0.0 1.57
```

This script:
- Starts the Docker container
- Opens Gazebo Harmonic with the B002 laboratory world (`sim/worlds/my_lab.sdf`)
- Opens RViz
- Launches TurtleBot 4 with SLAM and Nav2 (if enabled)

## Option 2: Manual Step-by-Step

1. **Start the container:**
   ```bash
   ./sim/run_docker.sh
   ```
2. **Inside the container:**
   ```bash
   source /opt/ros/jazzy/setup.bash
   ls -la /root/worlds/
   ./sim/run_lab_world.sh true true 0.0 0.0 0.0
   ```

## Useful Commands

- **Check topics:**
  ```bash
  ros2 topic list
  ros2 topic hz /scan
  ros2 topic echo /odom
  ```
- **Check TF:**
  ```bash
  ros2 run tf2_ros tf2_echo odom base_link
  ros2 run tf2_ros tf2_echo map base_link
  ```
- **Keyboard Teleop:**
  ```bash
  ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
  ```
- **Save Map:**
  ```bash
  ros2 run nav2_map_server map_saver_cli -f /root/maps/lab_map
  ```
