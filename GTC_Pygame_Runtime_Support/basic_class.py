#####
class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False

    def operate(self, mouse_pos, effectiveness):
        """

        :param mouse_pos:
        :type mouse_pos:            (int, int) | List[int, int]
        :param effectiveness:
        :type effectiveness:        bool
        :return:
        """
        self.do_cancel: bool = False

    def cancel(self):
        self.state = False
        self.do_cancel = True


class BasicChecker(object):
    def __init__(self, check_range, default_state = False):
        """
        :param check_range:             检查的范围
        :type check_range:              List[int] | Tuple[int, int]
        :param default_state:           默认状态
        :type default_state:            bool | int | str
        """
        self.range = check_range
        self.state = default_state

    def check(self, mouse_pos, mouse_click):
        pass

#####
