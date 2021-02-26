"""暂停按钮"""

import pygame
import constants as consts


class PauseButton:
    """暂停按钮类"""

    def __init__(self, window):
        """初始化暂停按钮"""

        # 加载鼠标没有移至状态的暂停图片
        self.image_pause_not_mouseover = pygame.image.load(
            'images/pause_not_mouseover.png')

        # 加载鼠标没有移至状态的继续图片
        self.image_resume_not_mouseover = pygame.image.load(
            'images/resume_not_mouseover.png')

        # 设置暂停按钮的初始图片是鼠标没有移至状态的暂停图片
        self.image = self.image_pause_not_mouseover

        # 获得暂停按钮的矩形
        self.rect = self.image.get_rect()

        # 设置暂停按钮的矩形的初始位置
        self.rect.top = consts.MARGIN
        self.rect.right = window.get_rect().right - consts.MARGIN

        # 标记游戏不处于暂停状态
        self.is_pause = False

    def switch_image(self):
        # 如果游戏不处于暂停状态
        if not self.is_pause:
            self.image = self.image_resume_not_mouseover
            self.is_pause = True
        # 如果游戏处于暂停状态
        else:
            self.image = self.image_pause_not_mouseover
            self.is_pause = False
