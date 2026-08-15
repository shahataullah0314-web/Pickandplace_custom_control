from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("moveit_resources_panda").to_dict()

    mtc_node = Node(
        package="mtc_tutorial",
        executable="mtc_node",
        output="screen",
        parameters=[moveit_config],
    )

    return LaunchDescription([mtc_node])
