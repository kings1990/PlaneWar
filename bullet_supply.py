"""子弹补给"""
import pygame
import random
from pygame.sprite import Sprite
import constants as consts


class BulletSupply(Sprite):
    # 子弹补给每次移动时的偏移量
    offset = 5

    def __init__(self, window):
        """初始化我方子弹补给"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载子弹补给图片
        self.image = pygame.image.load("images/bullet_supply.png")
        # 获得窗口对象
        self.window = window
        # 获得子弹补给的矩形
        self.rect = self.image.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置子弹补给的初始位置:窗口顶部随机位置
        self.rect.top = 0
        self.rect.left = random.randint(0, self.window_rect.width - self.rect.width)

    def update(self):
        """更新子弹补给位置"""
        # 减少矩形top使得向上移动
        self.rect.top += BulletSupply.offset

    def play_collide_sound(self):
        sound = pygame.mixer.Sound('sounds/bomb_supply_collide.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()

    @classmethod
    def update_offset(cls, pixels):
        BulletSupply.offset += pixels
