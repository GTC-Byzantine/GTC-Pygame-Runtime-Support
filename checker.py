from GTC_Pygame_Runtime_Support.basic_class import BasicChecker

class OnHover(BasicChecker):
    def __init__(self, check_range, default_state):
        super().__init__(check_range, default_state)

    def check(self, mouse_pos, mouse_click):
        self.state = False
        if self.range[0] <= mouse_pos[0] <= self.range[0] + self.range[2]\
                and self.range[1] <= mouse_pos[1] <= self.range[0] + self.range[3]:
            self.state = True
        return self.state

