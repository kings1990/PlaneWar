"""可视化炸弹组"""
import pygame
import random
import constants as consts


class VisualBombGroup:
    def __init__(self, window):
        """初始化我方炸弹补给"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载炸弹补给图片
        self.image = pygame.image.load("images/bomb.png")
        # 获得窗口对象
        self.window = window
        # 获得炸弹补给的矩形
        self.rect = self.image.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置炸弹补给的初始位置:窗口顶部随机位置
        self.rect.top = 0
        self.rect.left = random.randint(0, self.window_rect.width - self.rect.width)

        # 炸弹补给每次移动时的偏移量
        self.offset = 5

        # 初始炸弹数量
        self.bomb_number = 3

        # 炸弹图片矩形列表
        self.bomb_rect_list = []

        # 根据炸弹的初始数量将炸弹图片矩形定位在窗口中
        for i in range(self.bomb_number):
            # 获得炸弹的图片矩形
            bomb_rect = self.image.get_rect()
            bomb_rect.bottom = self.window_rect.height - consts.MARGIN
            # 设置炸弹矩形位置
            bomb_rect.right = (consts.MARGIN + bomb_rect.width) * (i + 1)
            # 将炸弹绘制再窗口上
            self.bomb_rect_list.append(bomb_rect)

    def play_explode_sound(self):
        sound = pygame.mixer.Sound('sounds/bomb_explode.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()
