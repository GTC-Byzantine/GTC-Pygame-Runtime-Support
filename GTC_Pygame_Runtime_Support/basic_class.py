from typing import List


class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False

    def operate(self, mouse_pos, effectiveness):
        """
        :param mouse_pos:
        :type mouse_pos:            (int, int) | List[int]
        :param effectiveness:
        :type effectiveness:        bool
        :return:
        """
        self.do_cancel: bool = False

    def cancel(self):
        self.state = False
        self.do_cancel = True


class BasicChecker(object):
    def __init__(self, check_range, default_state=False, do_reverse=False):
        """
        :param check_range:             检查的范围（横纵长宽）
        :type check_range:              List[int] | Tuple[int, int, int, int]
        :param default_state:           默认状态
        :type default_state:            bool | int | str
        """
        self.range = check_range
        self._state = default_state
        self._do_reverse = do_reverse

    def check(self, mouse_pos, mouse_click):
        """
        :param mouse_pos:
        :type mouse_pos:                        (int, int) | List[int]
        :param mouse_click:
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int]
        :return:
        """
        pass

    def change_range(self, check_range):
        self.range = check_range

    def add_pos(self, pos):
        self.range[0] = pos[0]
        self.range[1] = pos[1]


class BasicSurface:
    pass
