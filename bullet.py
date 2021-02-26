"""子弹"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, window, my_plane):
        """初始化子弹"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载子弹图片
        self.image = pygame.image.load("images/bullet.png")
        # 获得窗口对象
        self.window = window
        self.my_plane = my_plane
        # 获得我方飞机的矩形
        self.rect = self.image.get_rect()
        self.my_plane_rect = self.my_plane.rect

        # 设置子弹的初始位置:我方飞机的中顶部
        self.rect.midtop = self.my_plane_rect.midtop

        # 我方飞机每次移动时的偏移量
        self.offset = 50

    def update(self):
        """更新子弹位置"""
        # 减少矩形top使得向上移动
        self.rect.top -= self.offset
