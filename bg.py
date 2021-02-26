"""背景"""
import pygame


class Bg(object):
    """利用2张图片的移动模拟背景移动"""

    def __init__(self, window):
        """初始化背景"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载小型敌机图片
        self._load_images()
        # 获得窗口对象
        self.window = window
        # 获得小型敌机的矩形
        self.rect = self.bg.get_rect()
        self.rect1 = self.bg1.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置小型敌机的初始位置:窗口顶部随机位置
        self.rect.top = 0
        self.rect.left = 0

        # 小型敌机每次移动时的偏移量
        self.offset1 = 2
        self.offset2 = 1

    def _load_images(self):
        self.bg = pygame.image.load("images/bg.png")
        self.bg1 = pygame.image.load("images/bg.png")

    def update(self):
        """更新背景位置"""
        # 增加矩形top使得向下移动
        self.rect.top += self.offset1
        if self.rect.top >= self.rect.height:
            self.rect.top = 0
        self.rect1.top = self.rect.top - self.rect.height + self.offset2
        self.window.blit(self.bg, self.rect)
        self.window.blit(self.bg1, self.rect1)
