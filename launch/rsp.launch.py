# import os
# import xacro
# from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()
    ld.add_action(DeclareLaunchArgument('urdf_package', default_value='hv_bot',
                                        description='The package where the robot description is located.'))
    default_model_path = PathJoinSubstitution(['urdf', 'robot.urdf.xacro'])
    ld.add_action(DeclareLaunchArgument('urdf_model_path', default_value=default_model_path,
                                        description='The path to the robot description relative to the package root.'))
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value="true",
                                        description='Use sim time if true.'))
    
    package_dir = FindPackageShare(LaunchConfiguration('urdf_package'))
    model_path = PathJoinSubstitution([package_dir, LaunchConfiguration('urdf_model_path')])
    # model_path = os.path.join(get_package_share_directory('hv_bot'), 'urdf', 'robot.urdf.xacro')
    # doc = xacro.process_file(model_path, mappings={'use_sim' : LaunchConfiguration('use_sim_time')})
    # robot_description_content = doc.toprettyxml(indent='    ')
    
    robot_description_content = ParameterValue(Command(['xacro ', model_path]), value_type=str)
     
    robot_state_publisher_node = Node(package='robot_state_publisher',
                                      executable='robot_state_publisher',
                                      output='screen',
                                      parameters=[{
                                          'robot_description': robot_description_content,
                                          'use_sim_time': LaunchConfiguration('use_sim_time'),
                                      }])

    ld.add_action(robot_state_publisher_node)
    return ld