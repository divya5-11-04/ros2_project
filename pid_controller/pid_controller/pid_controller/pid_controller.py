#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class PIDController(Node):

    def __init__(self):

        super().__init__('pid_controller')

        # Desired speed
        self.target_velocity = 0.5

        # PID gains
        self.kp = 2.0
        self.ki = 0.01
        self.kd = 0.1

        # PID variables
        self.previous_error = 0.0
        self.integral = 0.0

        # Current velocity
        self.current_velocity = 0.0

        # Subscribe to odom
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publish cmd_vel
        self.cmd_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Control loop timer
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

    def odom_callback(self, msg):

        self.current_velocity = (
            msg.twist.twist.linear.x
        )

    def control_loop(self):

        # Calculate error
        error = (
            self.target_velocity
            - self.current_velocity
        )

        # Integral
        self.integral += error

        # Derivative
        derivative = (
            error - self.previous_error
        )

        # PID output
        output = (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )

        # Publish velocity
        twist = Twist()

        twist.linear.x = output
        twist.angular.z = 0.0

        self.cmd_publisher.publish(twist)

        # Save error
        self.previous_error = error

        # Console output
        self.get_logger().info(
            f'Current Velocity: '
            f'{self.current_velocity:.2f} | '
            f'Control Output: '
            f'{output:.2f}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = PIDController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()