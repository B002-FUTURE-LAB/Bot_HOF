# TurtleBot 4 Raspberry Pi 4 Configuration Backup (`192.168.0.129`)

This directory stores the live configuration files from the physical TurtleBot 4 Raspberry Pi 4 (`ubuntu@192.168.0.129`):

- `setup.bash`, `system`, `discovery.conf`, `discovery.sh`, `aliases.bash`, `chrony.conf` (from `/etc/turtlebot4/`)
- `fastdds_rpi.xml`, `fastdds_discovery_create3.xml`, `cyclonedds_rpi.xml` (from `/etc/turtlebot4/`)
- `oakd_pro.yaml` and `turtlebot4.yaml` (from `/opt/ros/jazzy/share/turtlebot4_bringup/config/`)

## Important Hardware Note (OAK-D Pro USB Stability)

In `oakd_pro.yaml`, `i_usb_speed` is set to `HIGH` (USB 2.0 High-Speed, 480 Mbps) and `i_laser_dot_brightness` is set to `0` to prevent USB 3.0 SuperSpeed enumeration brownouts (`X_LINK_ERROR` / `error -71`) on the Raspberry Pi 4 when battery voltage drops.
