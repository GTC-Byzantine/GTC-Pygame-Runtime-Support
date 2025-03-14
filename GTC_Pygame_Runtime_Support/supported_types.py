import typing
import pygame

Coordinate = typing.Union[typing.Tuple[float, float], typing.Sequence[float], pygame.Vector2]
_CanBeRect = typing.Union[
    pygame.Rect,
    typing.Tuple[typing.Union[float, int], typing.Union[float, int], typing.Union[float, int], typing.Union[float, int]],
    typing.Tuple[Coordinate, Coordinate],
    typing.Sequence[typing.Union[float, int]],
    typing.Sequence[Coordinate],
]
RGBAOutput = typing.Tuple[int, int, int, int]
ColorValue = typing.Union[pygame.Color, int, str, typing.Tuple[int, int, int], RGBAOutput, typing.Sequence[int]]
RectValue = typing.Union[_CanBeRect]
RectSupport = typing.Union[Coordinate, RectValue]
MousePosType = typing.Union[typing.List[int], typing.Tuple[int, int]]
MousePressType = typing.Union[typing.List[bool], typing.Tuple[bool, bool, bool], typing.Tuple[bool, bool, bool, bool, bool]]
