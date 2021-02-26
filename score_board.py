"""得分板"""

import pygame
import constants as consts


class ScoreBoard:
    def __init__(self, window):
        """初始化我方炸弹补给"""

        # 调用父类的特殊方法init
        super().__init__()

        # 获得窗口对象

        self.window = window
        # 获得炸弹补给的矩形
        self.window_rect = self.window.get_rect()

        # 分数
        self.current_score = 0

        # 获得指定字体和指定字体大小的对象
        self.font_36 = pygame.font.Font('fonts/wawa.ttf', consts.FONT_SIZE)

        self.highest_score = self.read_highest_score()

        # 当前关数
        self.current_level = 1

        # 增加速度标记为
        self.speed_flag = [False]

    def draw_score(self):
        text = '当前得分%s' % self.current_score
        current_score_surface = self.font_36.render(text, True, consts.WHITE_COLOR)
        self.current_score_surface_rect = current_score_surface.get_rect()
        self.current_score_surface_rect.top = consts.MARGIN
        self.current_score_surface_rect.left = consts.MARGIN
        self.window.blit(current_score_surface, self.current_score_surface_rect)

    def draw_highest_score(self):
        text = '最高得分%s' % self.highest_score
        highest_score_surface = self.font_36.render(text, True, consts.WHITE_COLOR)
        self.highest_score_surface_rect = highest_score_surface.get_rect()
        self.highest_score_surface_rect.top = self.current_score_surface_rect.bottom + consts.MARGIN
        self.highest_score_surface_rect.left = consts.MARGIN
        self.window.blit(highest_score_surface, self.highest_score_surface_rect)

    def draw_current_level(self):
        text = '当前关数%s' % self.current_level
        current_level_surface = self.font_36.render(text, True, consts.WHITE_COLOR)
        current_level_surface_rect = current_level_surface.get_rect()
        current_level_surface_rect.top = self.highest_score_surface_rect.bottom + consts.MARGIN
        current_level_surface_rect.left = consts.MARGIN
        self.window.blit(current_level_surface, current_level_surface_rect)

    def read_highest_score(self):
        """读取得分"""

        with open("txts/highest_score.txt") as file:
            return int(file.read())

    def save_current_score(self):
        """保存得分"""

        with open("txts/highest_score.txt", 'w') as file:
            file.write(str(self.current_score))

    def update_current_level(self):
        # 当分数大于斐波那契数列最后一位时等级加1
        while self.current_score > list(self.fib(self.current_level))[self.current_level - 1] and self.current_level <= 10:
            self.current_level += 1
            if len(self.speed_flag) < self.current_level:
                self.speed_flag.append(True)

    def fib(self, n):
        """斐波那契数列"""
        i = 0
        a, b = 100, 200
        while i < n:
            # 生成器需要使用yield关键字
            yield a
            a, b = b, a + b
            i += 1
