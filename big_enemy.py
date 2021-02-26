"""大型敌机"""
import pygame
import random
from pygame.sprite import Sprite
import constants as consts


class BigEnemy(Sprite):
    # 大型敌机每次移动时的偏移量
    offset = 2

    def __init__(self, window):
        """初始化我方大型敌机"""

        # 调用父类的特殊方法init
        super().__init__()
        # 加载大型敌机图片
        self._load_images()
        self.image = self.image_big1

        # 获得窗口对象
        self.window = window
        # 获得大型敌机的矩形
        self.rect = self.image.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置大型敌机的初始位置:窗口顶部随机位置
        self.rect.bottom = 0
        self.rect.left = random.randint(0, self.window_rect.width - self.rect.width)

        # 敌机图片切换
        self.switch_count = 0

        # 爆炸切换计数器
        self.switch_explode_count = 0
        # 击中切换计数器
        self.switch_hit_count = 0

        # 爆炸标记位
        self.explode_flag = False
        # 击中标记位
        self.hit_flag = False

        # 能量
        self.energy = consts.BIG_ENERGY

    def _load_images(self):
        self.image_big1 = pygame.image.load("images/big_enemy1.png")
        self.image_big2 = pygame.image.load("images/big_enemy2.png")
        self.image_explode1 = pygame.image.load("images/big_enemy_explode1.png")
        self.image_explode2 = pygame.image.load("images/big_enemy_explode2.png")
        self.image_explode3 = pygame.image.load("images/big_enemy_explode3.png")
        self.image_explode4 = pygame.image.load("images/big_enemy_explode4.png")
        self.image_explode5 = pygame.image.load("images/big_enemy_explode5.png")
        self.image_explode6 = pygame.image.load("images/big_enemy_explode6.png")
        self.hit_image = pygame.image.load("images/big_enemy_hit.png")

    def update(self):
        """更新大型敌机位置"""
        # 减少矩形top使得向上移动
        self.rect.top += BigEnemy.offset

    def play_explode_sound(self):
        sound = pygame.mixer.Sound('sounds/big_enemy_explode.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()

    def switch_image(self):
        """切换飞机图片"""

        self.switch_count += 1
        # 如果计数器加到3才切换一次我方飞机的图片
        if self.switch_count == consts.MID_ENEMY_SWITCH_IMAGE_FREQUENCY:
            # 如果是第一张图片则切换到第二张图片
            # 如果是第二张图片则切换到第一张图片
            if self.image == self.image_big1:
                self.image = self.image_big2
            elif self.image == self.image_big2:
                self.image = self.image_big1

            self.switch_count = 0

    def swich_explode_image(self):
        """切换中型敌机飞机图片"""

        self.switch_explode_count += 1
        # 如果计数器加到3才切换一次我方飞机的图片
        if self.switch_explode_count == consts.BIG_ENEMY_SWITCH_EXPLODE_IMAGE_FREQUENCY:
            if self.image == self.image_big1 or self.image == self.image_big2:
                self.image = self.image_explode1
            elif self.image == self.image_explode1:
                self.image = self.image_explode2
            elif self.image == self.image_explode2:
                self.image = self.image_explode3
            elif self.image == self.image_explode3:
                self.image = self.image_explode4
            elif self.image == self.image_explode4:
                self.image = self.image_explode5
            elif self.image == self.image_explode5:
                self.image = self.image_explode6
            else:
                # 将敌机从分组中删除
                self.kill()

            self.switch_explode_count = 0

    def draw_energy_lines(self):
        """绘制能量线"""

        # 在敌机尾部上分绘制红色线段
        # 白色线段
        pygame.draw.line(self.window, (208, 208, 208),
                         (self.rect.left, self.rect.top),
                         (self.rect.right, self.rect.top),
                         2)

        # 血量比
        energy_ratio = self.energy / consts.BIG_ENERGY
        # 红色线段(血量)
        if self.energy != 0:
            pygame.draw.line(self.window, (255, 0, 0),
                             (self.rect.left, self.rect.top),
                             (self.rect.left + self.rect.width * energy_ratio, self.rect.top),
                             2)

    def swich_hit_image(self):
        """切换中型敌机飞机图片"""

        self.switch_hit_count += 1
        # 如果计数器加到3才切换一次我方飞机的图片
        if self.switch_hit_count == consts.BIG_ENEMY_SWITCH_HIT_IMAGE_FREQUENCY:
            # 如果是第一张图片则切换到第二张图片
            # 如果是第二张图片则切换到第一张图片
            if self.image == self.image_big1 or self.image == self.image_big2:
                self.image = self.hit_image
            elif self.image == self.hit_image:
                self.image = self.image_big1
                # 重新标记到未被击中标记
                self.hit_flag = False

            self.switch_hit_count = 0

    @classmethod
    def update_offset(cls, pixels):
        BigEnemy.offset += pixels
