"""我方飞机"""
import pygame
from pygame.sprite import Sprite
import constants as consts
from math import pi


class MyPlane(Sprite):
    """我方飞机类"""

    def __init__(self, window):
        """初始化我方飞机"""

        # 调用父类的特殊方法init
        super().__init__()

        # 加载飞机图片
        self.image1 = pygame.image.load("images/my_plane1.png")
        self.image2 = pygame.image.load("images/my_plane2.png")
        self.my_plane_explode_img = pygame.image.load("images/my_plane_explode.png")
        self.image = self.image1

        # 获得窗口对象
        self.window = window

        # 获得我方飞机的矩形
        self.rect = self.image.get_rect()
        self.window_rect = self.window.get_rect()

        # 设置我方飞机的初始位置:窗口底部居中
        self.rect.midbottom = self.window_rect.midbottom

        # 向上移动标记
        self.move_up = False
        # 向上移动标记
        self.move_down = False
        # 向上移动标记
        self.move_left = False
        # 向上移动标记
        self.move_right = False
        # 我方飞机每次移动时的偏移量
        self.offset = 20
        # 飞机切换图片计数器
        self.switch_count = 1
        # 生命数
        self.life_num = consts.LIFE_NUM

        # 无敌状态
        self.is_invincible = False

        # 我方飞机生命图片
        self.life_image = pygame.transform.scale(self.image1, (round(self.rect.width / 3), round(self.rect.height / 3)))
        # 我方飞机生命图片矩形列表
        self.life_rect_list = []
        # 根据我方飞机的生命数,将对应数量的生命的图片矩形放入列表
        for i in range(self.life_num):
            life_rect = self.life_image.get_rect()
            # 设置我方飞机的生命图片矩形的初始位置
            life_rect.bottom = self.window_rect.height - consts.MARGIN
            life_rect.right = self.window_rect.width - consts.MARGIN - i * (
                    life_rect.width + consts.MARGIN)
            self.life_rect_list.append(life_rect)

    def update(self):
        """更新我方飞机位置"""
        if self.move_up and self.rect.top - self.offset > 0:
            self.rect.top -= self.offset
        if self.move_down and self.rect.bottom + self.offset < self.window_rect.height:
            self.rect.bottom += self.offset
        if self.move_left and self.rect.left - self.offset + self.rect.width / 5 * 3 > 0:
            self.rect.left -= self.offset
        # 左右移动的时候允许半个飞机身体出窗口界面保证可以打到边缘的飞机
        if self.move_right and self.rect.right + self.offset - self.rect.width / 5 * 3 < self.window_rect.width:
            self.rect.right += self.offset

    def draw(self):
        """在窗口中绘制我方飞机"""

        # 在窗口的底部居中位置绘制一架飞机
        self.window.blit(self.image, self.rect)

    def switch_image(self):
        """切换飞机图片"""

        self.switch_count += 1
        # 如果计数器加到3才切换一次我方飞机的图片
        if self.switch_count == consts.MY_PLANE_SWITCH_IMAGE_FREQUENCY:
            # 如果是第一张图片则切换到第二张图片
            # 如果是第二张图片则切换到第一张图片
            if self.image == self.image1:
                self.image = self.image2
            else:
                self.image = self.image1

            self.switch_count = 0

    def reset_position(self):
        """重置我方飞机位置"""

        # 设置我方飞机的初始位置:窗口底部居中
        self.rect.midbottom = self.window_rect.midbottom

    def draw_invincible(self, circle_percentage):
        """画无敌护盾"""

        # 圆从水平右侧点开始算0pi 逆时针转动逐级增加
        # 效果是从正上方开始顺时针护盾消失
        pygame.draw.arc(self.window, consts.INVINCIBLE_CIRCLE_COLOR, self.rect, pi / 2,
                        pi / 2 + pi * 2 * circle_percentage,
                        consts.INVINCIBLE_CIRCLE_WIDTH)

    def play_explode_sound(self):
        sound = pygame.mixer.Sound('sounds/plane_explore.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()

    def play_invincible_sound(self):
        sound = pygame.mixer.Sound('sounds/invincible.wav')
        sound.set_volume(consts.EXPLODE_SOUND_VOLUME)
        sound.play()
