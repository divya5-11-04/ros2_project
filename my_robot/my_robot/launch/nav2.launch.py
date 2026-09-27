#!/usr/bin/env python3
"""
Bring up Nav2 for the simulated restaurant service robot.

Two ways to run this:

1) LIVE MAPPING (map not saved yet):
     Run slam.launch.py in one terminal (produces /map, map->odom TF),
     then run THIS launch file with slam:=True so Nav2 skips its own
     map_server/AMCL and instead localizes off slam_toolbox's live map.

2) SAVED MAP (after running `ros2 run nav2_map_server map_saver_cli -f my_map`):
     Run this launch file with slam:=False and map:=/path/to/my_map.yaml.
     Nav2 will load the static map and localize with AMCL.

Usage:
  ros2 launch my_robot nav2.launch.py slam:=True
  ros2 launch my_robot nav2.launch.py slam:=False map:=/home/you/my_map.yaml
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    pkg_share = get_package_share_directory('my_robot')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    nav2_params_file = os.path.join(
        pkg_share, 'config', 'nav2_params.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    slam = LaunchConfiguration('slam')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation clock from Gazebo'
    )

    declare_slam = DeclareLaunchArgument(
        'slam', default_value='True',
        description='Run against slam_toolbox live map instead of a saved map + AMCL'
    )

    declare_map = DeclareLaunchArgument(
        'map', default_value='',
        description='Full path to map yaml file (only used when slam:=False)'
    )

    declare_params_file = DeclareLaunchArgument(
        'params_file', default_value=nav2_params_file,
        description='Full path to the Nav2 parameters file'
    )

    # nav2_bringup's bringup_launch.py handles map_server/AMCL vs slam mode,
    # controller_server, planner_server, behavior_server, bt_navigator,
    # waypoint_follower, velocity_smoother, and lifecycle manager for all of it.
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam': slam,
            'map': map_yaml_file,
            'params_file': params_file,
            'autostart': 'true',
        }.items()
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_slam,
        declare_map,
        declare_params_file,
        nav2_bringup_launch,
    ])
