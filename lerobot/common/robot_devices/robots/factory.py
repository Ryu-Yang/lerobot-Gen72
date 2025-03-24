import os


right_arm_ip = os.getenv("RIGHT_ARM_IP", "192.168.1.19")
left_arm_ip = os.getenv("LEFT_ARM_IP", "192.168.1.20")
right_larm_port = os.getenv("RIGHT_LARM_PORT", "/dev/ttyUSB0")
left_larm_port = os.getenv("LEFT_LARM_PORT", "/dev/ttyUSB1")

def make_robot(name):
    if name == "koch":
        # TODO(rcadene): Add configurable robot from command line and yaml config
        # TODO(rcadene): Add example with and without cameras
        from lerobot.common.robot_devices.cameras.opencv import OpenCVCamera
        from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
        from lerobot.common.robot_devices.robots.koch import KochRobot

        robot = KochRobot(
            leader_arms={
                "main": DynamixelMotorsBus(
                    port="/dev/ttyUSB0",
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl330-m077"),
                        "shoulder_lift": (2, "xl330-m077"),
                        "elbow_flex": (3, "xl330-m077"),
                        "wrist_flex": (4, "xl330-m077"),
                        "wrist_roll": (5, "xl330-m077"),
                        "gripper": (6, "xl330-m077"),
                    },
                ),
            },
            follower_arms={
                "main": DynamixelMotorsBus(
                    port="/dev/ttyUSB1",
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl430-w250"),
                        "shoulder_lift": (2, "xl430-w250"),
                        "elbow_flex": (3, "xl330-m288"),
                        "wrist_flex": (4, "xl330-m288"),
                        "wrist_roll": (5, "xl330-m288"),
                        "gripper": (6, "xl330-m288"),
                    },
                ),
            },
            cameras={
                "top": OpenCVCamera(0, fps=30, width=640, height=480),
                # "phone": OpenCVCamera(1, fps=30, width=640, height=480),
            },
        )
    elif name=="gen72":
        from lerobot.common.robot_devices.cameras.opencv import OpenCVCamera
        from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
        from lerobot.common.robot_devices.robots.koch import KochRobot

        robot = KochRobot(
            leader_arms={
                "main": DynamixelMotorsBus(
                    port="/dev/ttyUSB0",
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl330-m077"),
                        "shoulder_lift": (2, "xl330-m077"),
                        "elbow_flex": (3, "xl330-m077"),
                        "wrist_flex": (4, "xl330-m077"),
                        "wrist_roll": (5, "xl330-m077"),
                        "gripper": (6, "xl330-m077"),
                    },
                ),
            },
            cameras={
                "top": OpenCVCamera(0, fps=30, width=640, height=480),
                "phone": OpenCVCamera(2, fps=30, width=640, height=480),
            },
        )
    elif name=="gen72_leader":
        from lerobot.common.robot_devices.cameras.opencv import OpenCVCamera
        from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
        from lerobot.common.robot_devices.robots.koch import KochRobot

        robot = KochRobot(
            ip = "192.168.1.20",
            calibration_path = ".cache/calibration/left_arm.pkl",
            start_pose = [-90.0, 90.0, 90.0, -90.0, 0.0, 0.0, 0.0],
            joint_p_limit = [169.0, 102.0, 169.0, 52.0, 169.0, 117.0, 169.0],
            joint_n_limit = [-169.0, -102.0, -169.0, -167.0, -169.0, -87.0, -169.0],
            leader_arms={
                "main": DynamixelMotorsBus(
                    port="/dev/ttyUSB0",
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl330-m288"),
                        "shoulder_lift": (2, "xl330-m288"),
                        "elbow_flex": (3, "xl330-m288"),
                        "wrist_flex": (4, "xl330-m288"),
                        "wrist_roll": (5, "xl330-m288"),
                        "wrist_1": (6, "xl330-m288"),
                        "weist_2": (7, "xl330-m288"),
                        "gripper": (8, "xl330-m288"),
                    },
                ),
            },
        )
    elif name=="gen72_two_arms_leader":
        from lerobot.common.robot_devices.cameras.opencv import OpenCVCamera
        from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
        from lerobot.common.robot_devices.robots.koch import KochRobot

        right_robot = KochRobot(
            ip = right_arm_ip,
            calibration_path = ".cache/calibration/right_arm.pkl",
            start_pose = [90.0, 90.0, -90.0, -90.0, 0.0, 0.0, 0.0],
            joint_p_limit = [169.0, 102.0, 169.0, 52.0, 169.0, 117.0, 169.0],
            joint_n_limit = [-169.0, -102.0, -169.0, -167.0, -169.0, -87.0, -169.0],
            leader_arms = {
                "main": DynamixelMotorsBus(
                    port=right_larm_port,
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl330-m288"),
                        "shoulder_lift": (2, "xl330-m288"),
                        "elbow_flex": (3, "xl330-m288"),
                        "wrist_flex": (4, "xl330-m288"),
                        "wrist_roll": (5, "xl330-m288"),
                        "wrist_1": (6, "xl330-m288"),
                        "weist_2": (7, "xl330-m288"),
                        "gripper": (8, "xl330-m288"),
                    },
                ),
            },
        )
        left_robot = KochRobot(
            ip = left_arm_ip,
            calibration_path = ".cache/calibration/left_arm.pkl",
            start_pose = [-90.0, 90.0, 90.0, -90.0, 0.0, 0.0, 0.0],
            joint_p_limit = [169.0, 102.0, 169.0, 52.0, 169.0, 117.0, 169.0],
            joint_n_limit = [-169.0, -102.0, -169.0, -167.0, -169.0, -87.0, -169.0],
            leader_arms = {
                "main": DynamixelMotorsBus(
                    port=left_larm_port,
                    motors={
                        # name: (index, model)
                        "shoulder_pan": (1, "xl330-m288"),
                        "shoulder_lift": (2, "xl330-m288"),
                        "elbow_flex": (3, "xl330-m288"),
                        "wrist_flex": (4, "xl330-m288"),
                        "wrist_roll": (5, "xl330-m288"),
                        "wrist_1": (6, "xl330-m288"),
                        "weist_2": (7, "xl330-m288"),
                        "gripper": (8, "xl330-m288"),
                    },
                ),
            },
        )
        robot = right_robot, left_robot
    else:
        raise ValueError(f"Robot '{name}' not found.")

    return robot
