def get_true_color(r: int, g: int, b: int) -> list[float]:
    """Преобразует RGB 0-255 в значения 0.0-1.0"""
    return [r / 255, g / 255, b / 255]


def get_rand_color() -> list[float]:
    """Возвращает светло-серый цвет"""
    return [0.9, 0.9, 0.9]