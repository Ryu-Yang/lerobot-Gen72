class JointLimiter:
    def __init__(self):
        # 初始化关节的正负限位
        self.joint_p_limit = [172.0, 105.0, 172.0, 55.0, 172.0, 120.0, 172.0]
        self.joint_n_limit = [-172.0, -105.0, -172.0, -170.0, -172.0, -90.0, -172.0]
        # 初始化关节的目标值
        self.joint_teleop_write = [200.0, -150.0, 100.0, -180.0, 0.0, 130.0, -200.0]

    def limit_joints(self):
        # 限制关节值在正负限位之间
        for i in range(7):
            self.joint_teleop_write[i] = max(self.joint_n_limit[i], min(self.joint_p_limit[i], self.joint_teleop_write[i]))

    def print_joints(self):
        # 打印限制后的关节值
        print("限制后的关节值:", self.joint_teleop_write)


# 测试代码
if __name__ == "__main__":
    # 创建 JointLimiter 实例
    limiter = JointLimiter()
    print("初始关节值:", limiter.joint_teleop_write)

    # 限制关节值
    limiter.limit_joints()

    # 打印限制后的关节值
    limiter.print_joints()
