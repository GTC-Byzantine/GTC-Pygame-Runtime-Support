from GTC_Pygame_Runtime_Support.basic_class import *
from GTC_Pygame_Runtime_Support.supported_types import *
class InputBox(BasicInputBox):
    def __init__(self,
                 size: Coordinate,
                 pos: Coordinate,
                 surface: SurfaceType,
                 default_text: str='',
                 remind_text: str='',
                 background_color: ColorValue=(255, 255, 255),
                 border_color: List[ColorValue] | Tuple[ColorValue]=((0, 0, 0), (0, 112, 255)),
                 font_color: ColorValue=(0, 0, 0),
                 font_type: str='SimHei',
                 font_size: int=20,
                 remind_text_color: ColorValue=(160, 160, 160),
                 border_width: int=2,
                 border_radius: int=1,
                 fps: int=60,
                 cursor_color: ColorValue=(0, 0, 0),
                 select_area_color: List[ColorValue] | Tuple[ColorValue]=((51, 103, 209), (200, 200, 200)),
                 do_color_reverse: bool=True
                 ): ...
