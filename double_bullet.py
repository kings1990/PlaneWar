"""双发子弹"""
import pygame
from pygame.sprite import Sprite
import constants as consts


class DoubleBullet(Sprite):
    def __init__(self, window, my_plane):
        """初始化双发子弹"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载双发子弹图片
        self.image = pygame.image.load("images/double_bullet.png")
        # 获得窗口对象
        self.window = window
        self.my_plane = my_plane
        # 获得我方飞机的矩形
        self.rect = self.image.get_rect()
        self.my_plane_rect = self.my_plane.rect

        # 我方飞机每次移动时的偏移量
        self.offset = 50

    def update(self):
        """更新双发子弹位置"""
        # 减少矩形top使得向上移动
        self.rect.top -= self.offset

    def play_collide_sound(self):
        sound = pygame.mixer.Sound('sounds/bullet_supply_collide.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()
