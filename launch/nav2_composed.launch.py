"""Nav2 em um único participant DDS para o TurtleBot 4.

O Discovery Server do robô pode entregar tópicos do robô normalmente, mas
falhava de forma intermitente ao fazer o lifecycle_manager descobrir os
serviços de dez processos Nav2 criados ao mesmo tempo.  Os mesmos componentes
são carregados no container oficial do Nav2, portanto o lifecycle manager e
os servidores partilham um participant DDS e não dependem dessa descoberta
entre processos locais.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LoadComposableNodes, Node, SetParameter
from launch_ros.descriptions import ComposableNode, ParameterFile
from nav2_common.launch import RewrittenYaml

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    autostart = LaunchConfiguration("autostart")
    log_level = LaunchConfiguration("log_level")

    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites={"autostart": autostart},
            convert_types=True,
        ),
        allow_substs=True,
    )
    remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]
    # route_server não participa de NavigateToPose e, neste ambiente Jazzy,
    # perde o heartbeat e derruba toda a árvore lifecycle durante uma meta.
    # O opennav_docking também não participa do protocolo deste projeto: o
    # acoplamento físico é feito pela action /dock da Create 3. Nesta imagem
    # Jazzy ele causa SIGSEGV na configuração e derruba o container inteiro.
    lifecycle_nodes = [
        "controller_server", "smoother_server", "planner_server",
        "behavior_server", "velocity_smoother", "collision_monitor",
        "bt_navigator", "waypoint_follower",
    ]

    container = Node(
        package="rclcpp_components",
        executable="component_container",
        name="nav2_container",
        output="screen",
        arguments=["--ros-args", "--log-level", log_level],
    )

    component_params = [configured_params, {"use_sim_time": use_sim_time}]
    navigation = LoadComposableNodes(
        target_container=(namespace, "/nav2_container"),
        composable_node_descriptions=[
            ComposableNode(package="nav2_controller", plugin="nav2_controller::ControllerServer", name="controller_server", parameters=component_params, remappings=remappings + [("cmd_vel", "cmd_vel_nav")]),
            ComposableNode(package="nav2_smoother", plugin="nav2_smoother::SmootherServer", name="smoother_server", parameters=component_params, remappings=remappings),
            ComposableNode(package="nav2_planner", plugin="nav2_planner::PlannerServer", name="planner_server", parameters=component_params, remappings=remappings),
            ComposableNode(package="nav2_behaviors", plugin="behavior_server::BehaviorServer", name="behavior_server", parameters=component_params, remappings=remappings + [("cmd_vel", "cmd_vel_nav")]),
            ComposableNode(package="nav2_bt_navigator", plugin="nav2_bt_navigator::BtNavigator", name="bt_navigator", parameters=component_params, remappings=remappings),
            ComposableNode(package="nav2_waypoint_follower", plugin="nav2_waypoint_follower::WaypointFollower", name="waypoint_follower", parameters=component_params, remappings=remappings),
            ComposableNode(package="nav2_velocity_smoother", plugin="nav2_velocity_smoother::VelocitySmoother", name="velocity_smoother", parameters=component_params, remappings=remappings + [("cmd_vel", "cmd_vel_nav")]),
            ComposableNode(package="nav2_collision_monitor", plugin="nav2_collision_monitor::CollisionMonitor", name="collision_monitor", parameters=component_params, remappings=remappings),
            # Os componentes compartilham este mesmo processo. Mesmo assim,
            # os bonds ROS ainda dependem do executor receber CPU. O padrão
            # de 4 s derrubava a pilha inteira sob carga gráfica e abortava
            # uma meta legítima. Trinta segundos detecta uma queda real sem
            # transformar jitter temporário em falha crítica.
            ComposableNode(
                package="nav2_lifecycle_manager",
                plugin="nav2_lifecycle_manager::LifecycleManager",
                name="lifecycle_manager_navigation",
                parameters=[{
                    "autostart": autostart,
                    "node_names": lifecycle_nodes,
                    "bond_timeout": 30.0,
                    "bond_respawn_max_duration": 60.0,
                    "attempt_respawn_reconnection": True,
                }],
            ),
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument("namespace", default_value=""),
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("params_file", description="Arquivo de parâmetros Nav2"),
        DeclareLaunchArgument("autostart", default_value="true"),
        DeclareLaunchArgument("log_level", default_value="info"),
        container,
        # O container precisa criar o serviço de carga antes de receber os
        # componentes; não há espera DDS entre cada servidor Nav2.
        TimerAction(period=1.0, actions=[SetParameter("use_sim_time", use_sim_time), navigation]),
    ])
