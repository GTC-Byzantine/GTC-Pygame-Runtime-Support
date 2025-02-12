from GTC_Pygame_Runtime_Support.basic_class import BasicChecker


class OnHover(BasicChecker):
    def __init__(self, check_range, default_state):
        super().__init__(check_range, default_state)

    def check(self, mouse_pos, mouse_click):
        self._state = False
        if self.range[0] <= mouse_pos[0] <= self.range[0] + self.range[2] \
                and self.range[1] <= mouse_pos[1] <= self.range[0] + self.range[3]:
            self._state = True
        return self._state if not self._do_reverse else not self._do_reverse


class AlwaysTrue(BasicChecker):
    def __init__(self, check_range, default_state=False, do_reverse=False):
        super().__init__(check_range, default_state, do_reverse)

    def check(self, mouse_pos, mouse_click):
        return False if self._do_reverse else True
