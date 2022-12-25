


import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
    pkg_dir = get_package_share_directory('my_sphere_pkg') 

    # SDF
    sdf_file_name = 'sdf/sphere_goal/model.sdf'
    sdf = os.path.join(pkg_dir, 'models', sdf_file_name)
    
    spawn_entity = Node(package='gazebo_ros', 
                        executable='spawn_entity.py', 
                        arguments=['-entity', 'my_sphere', '-file', sdf, '-x','0.5', '-y','0.5', '-z','1'], 
                        output='screen')

    # Nodes
    # node_mark --> coordinate_node.py --> reads the position of the sphere in Gazebo and publishes the Marker Topic 
    
    node_mark = Node(package ='my_sphere_pkg', executable ='reader_mark_node', output ='screen')
    
    return LaunchDescription([spawn_entity, node_mark])
