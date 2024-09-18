import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    launch_package = FindPackageShare('hv_bot')
    
    rsp = IncludeLaunchDescription(
        PathJoinSubstitution([launch_package, 'launch', 'rsp.launch.py']),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
        
    world_path = os.path.join(get_package_share_directory('hv_bot'), 'worlds', 'obstacles.sdf')
    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']),
        launch_arguments={'gz_args': '-r ' + world_path}.items(),
    )
    # Run the create(spawner) node from the ros_gz_sim package. The name doesn't really matter if you only have a single robot.
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        parameters=[{'world': 'my_world',
                     'topic': 'robot_description',
                     'name': 'hv_bot',
                     'z': 0.05}],
    )
    # Run Bridge to communicate between ros and gazebo sim
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                   '/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                   '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                   '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
                   '/depth_camera@sensor_msgs/msg/Image@gz.msgs.Image',
                   '/depth_camera/ponit@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked'],
        output='screen',
    )
    
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        bridge,
    ])