# ROS 2 Restaurant Service Robot Simulation

A Python-based ROS 2 simulation of a differential-drive restaurant service robot. The project combines an SDF/URDF robot model, Gazebo simulation, ROS–Gazebo bridges, LiDAR perception, odometry, SLAM Toolbox, Nav2, and a basic velocity PID controller.

## Capabilities

- Simulated differential-drive robot in a restaurant-style world
- Robot description in URDF and SDF
- LiDAR data on `/scan`
- Odometry on `/odom`
- Velocity commands on `/cmd_vel`
- ROS–Gazebo communication through `ros_gz_bridge`
- RViz2 visualization
- Live mapping with SLAM Toolbox
- Navigation with Nav2 using either a live SLAM map or a saved map
- Optional Python PID controller for forward-velocity regulation

## Repository layout

```text
ros2_project/
├── my_robot/
│   └── my_robot/
│       ├── config/
│       │   ├── nav2_params.yaml
│       │   └── slam_toolbox_params.yaml
│       ├── launch/
│       │   ├── nav2.launch.py
│       │   └── slam.launch.py
│       ├── models/
│       │   └── my_robot.sdf
│       ├── urdf/
│       │   └── my_robot.urdf
│       └── worlds/
│           ├── robotworld.sdf
│           └── world.sdf
└── pid_controller/
    └── pid_controller/
        └── pid_controller/
            └── pid_controller.py
```

## Requirements

- Ubuntu with ROS 2 Humble (or a compatible ROS 2 distribution)
- Gazebo / Ignition Gazebo
- `ros_gz_bridge`
- `slam_toolbox`
- `nav2_bringup`
- RViz2
- Python 3 with `setuptools`

Source ROS 2 before building and install any missing ROS dependencies with `rosdep` where available.

## Build

From the repository root, use the package directories as the source workspace:

```bash
mkdir -p ~/ros2_ws/src
cp -r my_robot ~/ros2_ws/src/
cp -r pid_controller ~/ros2_ws/src/
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

> The packages are stored under `my_robot/my_robot` and `pid_controller/pid_controller`; copy those package directories into `src` as shown above.

## Run the simulation

Start Gazebo with the included restaurant world. From the package's world directory, run:

```bash
ign gazebo ~/ros2_ws/src/my_robot/my_robot/worlds/robotworld.sdf
```

Start the required bridges in separate terminals. Source ROS 2 and the workspace in each terminal first:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
```

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry'
```

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
```

Open RViz2 to inspect the robot, TF frames, odometry, and LiDAR data:

```bash
rviz2
```

## SLAM Toolbox

The SLAM launch file starts asynchronous SLAM Toolbox and uses simulation time. Gazebo and the `/cmd_vel`, `/odom`, and `/scan` bridges must already be running:

```bash
ros2 launch my_robot slam.launch.py
```

The launch file expects the robot to provide the appropriate odometry and TF relationships, including `odom` to `base_link`.

## Nav2

### Live mapping

Run SLAM Toolbox first, then launch Nav2 in SLAM mode:

```bash
ros2 launch my_robot nav2.launch.py slam:=True
```

### Saved map

After creating a map, save it with Nav2's map saver:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

Then launch Nav2 with the saved map:

```bash
ros2 launch my_robot nav2.launch.py \
  slam:=False map:=/home/$USER/my_map.yaml
```

The Nav2 launch file loads `nav2_params.yaml` and starts the standard Nav2 bringup components, including localization, planning, control, behavior, and lifecycle management as configured.

## PID controller

The `pid_controller` node subscribes to `/odom`, compares the measured forward velocity with a target of `0.5 m/s`, and publishes a control command to `/cmd_vel` at a 10 Hz control rate.

The current gains are defined in `pid_controller.py`:

- `Kp = 2.0`
- `Ki = 0.01`
- `Kd = 0.1`

The package currently contains the node implementation; if a console entry point is added to `setup.py`, it can be started with:

```bash
ros2 run pid_controller pid_controller
```

## ROS 2 interfaces

| Interface | Type | Purpose |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Robot velocity command |
| `/odom` | `nav_msgs/msg/Odometry` | Robot pose and velocity estimate |
| `/scan` | `sensor_msgs/msg/LaserScan` | LiDAR scan data |
| `/tf` | `tf2_msgs/msg/TFMessage` | Coordinate-frame transforms |

## Development checks

Both packages include the standard ROS 2 Python test configuration for copyright, Flake8, PEP 257, and pytest checks. After building, run:

```bash
colcon test
colcon test-result --verbose
```

## Project status and next steps

The repository provides the simulation, sensing, SLAM, Nav2 launch configuration, and initial PID control implementation. Potential next steps include tuning the controller, adding an installed console entry point, saving and validating maps, waypoint-based restaurant delivery, obstacle avoidance, and a complete autonomous serving workflow.

## License

The `my_robot` package includes an Apache-2.0 license. Review the package metadata before redistributing the complete project because the `pid_controller` package currently has a placeholder license declaration.
