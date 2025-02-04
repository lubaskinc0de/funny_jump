from pygame import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite


class BoundedSprite(Sprite):
    rect: Rect
    image: Surface
