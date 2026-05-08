# Restaurant Service Robot Simulation using ROS2 & Ignition Gazebo

## Overview

This project demonstrates the design and simulation of an autonomous mobile service robot using:

* Creo CAD
* ROS2
* Ignition Gazebo
* RViz

The robot is designed as a differential drive mobile robot capable of:

* localization,
* perception,
* odometry estimation,
* LiDAR sensing,
* and SLAM preprocessing.

The simulation environment represents a restaurant scenario where the robot can navigate indoors for future autonomous serving applications.

---

# Project Workflow

```text
Creo CAD Design
       ↓
URDF Robot Modeling
       ↓
Ignition Gazebo Simulation
       ↓
ROS2 Integration
       ↓
Odometry Implementation
       ↓
LiDAR Sensor Integration
       ↓
RViz Visualization
       ↓
SLAM Preprocessing
```

---

# Features

* Differential drive mobile robot
* Custom restaurant world simulation
* URDF-based robot model
* Ignition Gazebo integration
* RViz visualization
* Odometry implementation using `/odom`
* LiDAR sensor integration using `/scan`
* SLAM preprocessing pipeline
* ROS2 topic communication
* Real-time robot movement and perception

---

# Technologies Used

| Technology      | Purpose                |
| --------------- | ---------------------- |
| Creo            | CAD Modeling           |
| ROS2 Humble     | Robotics Middleware    |
| Ignition Gazebo | Robot Simulation       |
| RViz2           | Visualization          |
| URDF            | Robot Description      |
| LiDAR           | Environment Perception |
| Python          | ROS2 Nodes & Control   |

---

# Robot Architecture

## Differential Drive Robot

The robot uses:

* Left wheel
* Right wheel
* Differential drive control

Velocity commands are published through:

```bash
/cmd_vel
```

---

# Simulation Environment

A custom restaurant world was developed containing:

* walls,
* tables,
* indoor pathways,
* service area layout.

The environment is simulated in Ignition Gazebo.

---

# Odometry

Odometry was implemented using wheel motion data.

The robot continuously publishes:

* position,
* orientation,
* linear velocity,
* angular velocity

through:

```bash
/odom
```

Odometry data is visualized in RViz using trajectory visualization.

---

# LiDAR Integration

A LiDAR sensor was added to the robot for environment perception.

The sensor publishes real-time scan data through:

```bash
/scan
```

The scan data detects:

* walls,
* obstacles,
* nearby structures,
* environment boundaries.

Laser scan data is visualized in RViz as a point cloud.

---

# SLAM Preprocessing

The LiDAR scan data and odometry information form the preprocessing stage for SLAM (Simultaneous Localization and Mapping).

This project establishes the foundation for:

* autonomous navigation,
* occupancy grid mapping,
* path planning,
* obstacle avoidance.

---

# ROS2 Topics Used

| Topic      | Description                 |
| ---------- | --------------------------- |
| `/cmd_vel` | Robot velocity commands     |
| `/odom`    | Odometry information        |
| `/scan`    | LiDAR scan data             |
| `/tf`      | Coordinate frame transforms |

---

# Project Structure

```text
ros2_ws/
│
├── src/
│   ├── my_robot/
│   │   ├── urdf/
│   │   ├── worlds/
│   │   ├── launch/
│   │   ├── rviz/
│   │   └── meshes/
│   │
│   └── pid_controller/
│
└── install/
```

---

# Running the Project

## 1. Launch Ignition Gazebo

```bash
ign gazebo robotworld.sdf
```

---

## 2. Start ROS-GZ Bridges

### cmd_vel Bridge

```bash
ros2 run ros_gz_bridge parameter_bridge \
/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist
```

### Odometry Bridge

```bash
ros2 run ros_gz_bridge parameter_bridge \
/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry
```

### Laser Scan Bridge

```bash
ros2 run ros_gz_bridge parameter_bridge \
/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan
```

---

## 3. Open RViz

```bash
rviz2
```

---

# RViz Visualization

The following are visualized in RViz:

* Robot model
* Odometry trajectory
* LiDAR scan data
* Coordinate transforms

---

# Future Scope

* Complete SLAM mapping
* Autonomous navigation
* Nav2 integration
* Waypoint navigation
* Obstacle avoidance
* Autonomous restaurant serving
* PID-based motion control

---

# Results

The project successfully demonstrates:

* robot simulation,
* odometry implementation,
* LiDAR perception,
* ROS2 communication,
* and RViz visualization.

The robot can:

* move in a simulated restaurant environment,
* publish odometry data,
* detect surroundings using LiDAR,
* and visualize perception data in real time.

---

# Conclusion

This project demonstrates a complete robotics simulation pipeline starting from CAD modeling to ROS2-based perception and localization.

The integration of:

* Creo,
* URDF,
* Ignition Gazebo,
* ROS2,
* RViz,
* and LiDAR sensing

creates a strong foundation for future autonomous robotics applications such as SLAM and navigation.

---

