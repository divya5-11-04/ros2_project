#!/usr/bin/env python3
"""
Launch file to run slam_toolbox (async mode) against the simulated
differential-drive robot in this workspace.

Assumes:
  - Gazebo is already running with robotworld.sdf
  - ros_gz_bridge is already bridging /cmd_vel, /odom, /scan
  - robot publishes odom -> base_link TF (via odometry bridge / robot_state_publisher)

Usage:
  ros2 launch my_robot slam.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'my_robot'
    pkg_share = get_package_share_directory(package_name)

    slam_params_file = os.path.join(
        pkg_share, 'config', 'slam_toolbox_params.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock published by Gazebo'
    )

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        declare_use_sim_time,
        slam_toolbox_node,
    ])
