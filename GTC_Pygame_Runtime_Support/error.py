error0x01 = '滚轮支持开启后，mouse_wheel_status 应为(bool, bool)而非 None'
error0x02 = '参数应为 {} 的实例'


class UnexpectedParameter(Exception):
    def __init__(self, info):
        super().__init__()
        self.info = info

    def __str__(self):
        return self.info
