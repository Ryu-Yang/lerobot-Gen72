from lerobot.common.robot_devices.motors.dynamixel import (
    DriveMode,
    DynamixelMotorsBus,
    OperatingMode,
    TorqueMode,
)
from lerobot.common.robot_devices.motors.utils import MotorsBus

import numpy as np
import time
from pynput import keyboard



# 摩擦力力矩 N.m
C = 0.012

# P比例
P = 1

K = 0.5

# 电流值差异大于5mA
BIOS = 0.005

STEP = 300

INTERVAL = 0.001

#重置电机的状态，禁用扭矩模式，设置伺服电机的模式
def reset_arm(arm: MotorsBus):
    # To be configured, all servos must be in "torque disable" mode
    # arm.write("Torque_Enable", TorqueMode.DISABLED.value)#将所有伺服电机的扭矩模式设置为禁用，以确保电机在重置过程中不会施加力量。

    # Use 'extended position mode' for all motors except gripper, because in joint mode the servos can't
    # rotate more than 360 degrees (from 0 to 4095) And some mistake can happen while assembling the arm,
    # you could end up with a servo with a position 0 or 4095 at a crucial point See [
    # https://emanual.robotis.com/docs/en/dxl/x/x_series/#operating-mode11]
    # all_motors_except_gripper = [name for name in arm.motor_names if name != "gripper"]
    # arm.write("Operating_Mode", OperatingMode.EXTENDED_POSITION.value, all_motors_except_gripper)

    # TODO(rcadene): why?
    # Use 'position control current based' for gripper
    arm.write("Operating_Mode", OperatingMode.CURRENT_CONTROLLED_POSITION.value, "shoulder_pan")

    # Make sure the native calibration (homing offset abd drive mode) is disabled, since we use our own calibration layer to be more generic
    # arm.write("Homing_Offset", 0)
    # arm.write("Drive_Mode", DriveMode.NON_INVERTED.value)

class GravityCompensator:
    def __init__(self):
        # 机械臂参数 (示例值，需根据实际机械臂修改)
        self.m = [0.040, 0.8]     # 连杆质量 [kg]
        self.l = [0.16, 0.25]    # 连杆长度 [m]
        self.g = 9.81           # 重力加速度 [m/s²]
        self.com = [0.04, 0.1]  # 质心位置（距离前关节的距离）

    def compute_torques(self, q):
        """
        计算重力补偿力矩
        输入：
            q : 关节角度 [rad] (q1, q2)
        输出：
            tau : 关节力矩 [Nm] (tau1, tau2)
        """
        q1, q2 = q
        
        # 第一连杆对关节1的力矩
        tau1 = (self.m[0] * self.g * np.cos(q1) * self.com[0])
        
        # # 第二连杆对关节1的力矩
        # tau1 += self.m[1] * self.g * (
        #     self.l[0] * np.cos(q1) + 
        #     self.com[1] * np.cos(q1 + q2))
        
        # 第二连杆对关节2的力矩
        tau2 = self.m[1] * self.g * self.com[1] * np.cos(q1 + q2)
        
        return np.array([tau1, tau2])

# 使用示例
if __name__ == "__main__":
    compensator = GravityCompensator()
    leader_arm = DynamixelMotorsBus(
        port="/dev/ttyUSB0",
        motors={
            # name: (index, model)
            "shoulder_pan": (1, "xl330-m077"),
            # "shoulder_lift": (2, "xl330-m077"),
            # "elbow_flex": (3, "xl330-m077"),
            # "wrist_flex": (4, "xl330-m077"),
            # "wrist_roll": (5, "xl330-m077"),
            # "gripper": (6, "xl330-m077"),
        },
    )
    


    # reset_arm(leader_arm)
    leader_arm.connect()
    leader_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
    
    print("Save Home")
    input("Press Enter to continue...")

    value = leader_arm.read("Present_Position")
    processed_value = round(((value[0]) / 1024) * 90, 2)
    nearest_90 = round(processed_value / 90) * 90
    home = nearest_90
    print(f"Present_Position = {processed_value}")
    print(f"nearest_90 = {nearest_90}")

    # leader_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
    leader_arm.write("Torque_Enable", TorqueMode.ENABLED.value)
    leader_arm.write("Operating_Mode", OperatingMode.CURRENT_CONTROLLED_POSITION.value, "shoulder_pan")


    while True:
        

        Position_value = leader_arm.read("Present_Position")

        processed_value = round(((Position_value[0]) / 1024) * 90, 2)- home
        print(f"\nPresent_Position = {processed_value}")

        # 测试位置：关节角度（30度和60度）
        q_test = np.deg2rad([processed_value , 0])
        
        # 计算补偿力矩
        tau = compensator.compute_torques(q_test)
        
        print(f"补偿力矩: tau1={tau[0]:.5f} Nm, tau2={tau[1]:.5f} Nm")

        
        if tau[0] > 0:
            d_tau = (max(tau[0], C) - C)
        else:
            d_tau = (min(tau[0], -C) + C)

        current = d_tau/(K*P)

        print(f"补偿预估电流: current={current:.5f} A")

        value = leader_arm.read("Present_Current")
        
        print(f"value ={value}")
        if value[0] >> 15 == 1:
            print(f"进入负区间")
            buma = value[0]  # 补码（这里实际上只是获取 value[0] 的值）
            fanma = value[0] - 1  # 反码（这里实际上是 value[0] 减 1）
            yuanma = int(format(~fanma & 0xFFFF, '016b'), 2)  # 原码（这里是对 fanma 进行按位取反操作）  

            # print(f"补码: {buma}")
            # print(f"反码: {fanma}")
            # print(f"原码: {yuanma}")

            # # 将结果转换为 16 位二进制形式
            # def to_16bit_binary(num):
            #     return format(num & 0xFFFF, '016b')  # 使用掩码 0xFFFF 确保 16 位

            # print(f"补码: {to_16bit_binary(buma)}")
            # print(f"反码: {to_16bit_binary(fanma)}")
            # print(f"原码: {to_16bit_binary(yuanma)}")

            # num = int(yuanma, 2)
            p_current = yuanma * -0.001
        else:
            p_current = float(value[0])*0.001
        print(f"舵机当前电流: p_current={p_current:.5f} A")

        error = p_current - current
        if(abs(error)<=BIOS):
            error = 0
        else:
            goal_pose = Position_value + int(error*STEP)
            leader_arm.write("Goal_Position", goal_pose)
        time.sleep(INTERVAL)

        # if keyboard.is_pressed('q'):
        #     break
        # if keyboard.is_pressed('w'):
        #     leader_arm.write("Torque_Enable", TorqueMode.ENABLED.value)
        
        # if keyboard.is_pressed('e'):
        #     leader_arm.write("Torque_Enable", TorqueMode.DISABLED.value)

        # leader_arm.write("Torque_Enable", TorqueMode.ENABLED.value)
        
        # value = leader_arm.read("Present_Position")

        # leader_arm.write("Goal_Position", value)
        # time.sleep(0.001)