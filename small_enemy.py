"""小型敌机"""
import pygame
import random
from pygame.sprite import Sprite
import constants as consts


class SmallEnemy(Sprite):
    """小型敌机"""

    # 小型敌机每次移动时的偏移量
    offset = 6

    def __init__(self, window):
        """初始化我方小型敌机"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载小型敌机图片
        self._load_images()
        # 获得窗口对象
        self.window = window
        # 获得小型敌机的矩形
        self.rect = self.image.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置小型敌机的初始位置:窗口顶部随机位置
        self.rect.top = 0
        self.rect.left = random.randint(0, self.window_rect.width - self.rect.width)

        # 爆炸切换计数器
        self.switch_explode_count = 0

        # 爆炸标记位
        self.explode_flag = False

    def _load_images(self):
        self.image = self.image_small = pygame.image.load("images/small_enemy.png")
        self.image_explode1 = pygame.image.load("images/small_enemy_explode1.png")
        self.image_explode2 = pygame.image.load("images/small_enemy_explode2.png")
        self.image_explode3 = pygame.image.load("images/small_enemy_explode3.png")
        self.image_explode4 = pygame.image.load("images/small_enemy_explode4.png")

    def update(self):
        """更新小型敌机位置"""
        # 减少矩形top使得向上移动
        self.rect.top += SmallEnemy.offset

    def play_explode_sound(self):
        sound = pygame.mixer.Sound('sounds/small_enemy_explode.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()

    def swich_explode_image(self):
        """切换飞机图片"""

        self.switch_explode_count += 1
        # 如果计数器加到3才切换一次我方飞机的图片
        if self.switch_explode_count == consts.SMALL_ENEMY_SWITCH_EXPLODE_IMAGE_FREQUENCY:
            # 如果是第一张图片则切换到第二张图片
            # 如果是第二张图片则切换到第一张图片
            if self.image == self.image_small:
                self.image = self.image_explode1
            elif self.image == self.image_explode1:
                self.image = self.image_explode2
            elif self.image == self.image_explode2:
                self.image = self.image_explode3
            elif self.image == self.image_explode3:
                self.image = self.image_explode4
            else:
                # 将小型敌机从分组中删除
                self.kill()

            self.switch_explode_count = 0

    @classmethod
    def update_offset(cls, pixels):
        SmallEnemy.offset += pixels
