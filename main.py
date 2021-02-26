import pygame
import sys

from my_plane import MyPlane
from small_enemy import SmallEnemy
from mid_enemy import MidEnemy
from big_enemy import BigEnemy
from bullet import Bullet
from double_bullet import DoubleBullet
from bomb_supply import BombSupply
import constants as consts
from pygame.sprite import Group
from bullet_supply import BulletSupply
from bg import Bg
from visual_bomb_group import VisualBombGroup
from score_board import ScoreBoard
from pause_button import PauseButton


class PlaneWar:
    def __init__(self):
        pygame.init()

        self.t = 0
        # 创建窗口
        self._create_window()

        # 设置窗口
        self._set_window()

        # 播放背景音乐
        self._play_bg_music()

        # 背景
        self.bg = Bg(self.window)
        # 创建一架我方飞机
        self.my_plane = MyPlane(self.window)

        # 可视化炸弹组
        self.visual_bomb_group = VisualBombGroup(self.window)

        # 创建一个用于跟踪时间的时钟对象
        self.clock = pygame.time.Clock()

        # 创建管理画面的元素
        self._create_groups()

        # 设置定时器
        self._set_timers()

        # 游戏是否结束
        self.is_game_over = False

        # 无敌护盾圆百分比
        self.circle_percentage = 1

        # 获得指定字体和指定字体大小的对象
        self.font_36 = pygame.font.Font('fonts/wawa.ttf', consts.FONT_SIZE)

        # 双发子弹计数器
        self.double_bullet_counter = 0

        # 得分板
        self.score_board = ScoreBoard(self.window)

        self.pause_button = PauseButton(self.window)

    @staticmethod
    def get_window_size():
        info = pygame.display.Info()
        window_width = info.current_w
        window_height = info.current_h
        return window_width, window_height

    def _create_window(self):
        """创建窗口"""

        # 获取窗口尺寸
        window_width, window_height = self.get_window_size()
        # 屏幕宽度的2/5 高度的4/5为最合适
        screen_width, screen_height = window_width * consts.SCALE_HORIZONTAL, window_height * consts.SCALE_VERTICAL
        # 设定指定尺寸的窗口
        screen_width = 480
        screen_height = 800
        self.window = pygame.display.set_mode((round(screen_width), round(screen_height)))
        # self.window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    def _set_window(self):
        """设置窗口"""
        pygame.display.set_caption('飞机大战')
        self.plane_img = pygame.image.load("images/my_plane1.png")
        pygame.display.set_icon(self.plane_img)
        # 设置窗口背景颜色
        # self.window.fill(pygame.Color("lightskyblue"))

    def _create_groups(self):
        """创建管理精灵的分组"""

        # 子弹分组
        self.bullet_group = Group()
        # 子弹分组
        self.double_bullet_group = Group()
        # 子弹补给分组
        self.bullet_supply_group = Group()
        # 小型敌机分组
        self.small_enemy_group = Group()
        # 中型敌机分组
        self.mid_enemy_group = Group()
        # 中型敌机分组
        self.big_enemy_group = Group()
        # 敌机分组
        self.enemy_group = Group()
        # 炸弹分组
        self.bomb_group = Group()

    @staticmethod
    def _set_timers():
        """设置定时器"""

        # 自动发射子弹事件
        pygame.time.set_timer(consts.ID_OF_CREATE_BULLET, consts.INTERVAL_OF_CREATE_BULLET)
        # 自动创建小型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_SMALL_ENEMY, consts.INTERVAL_OF_CREATE_SMALL_ENEMY)
        # 自动创建中型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_MID_ENEMY, consts.INTERVAL_OF_CREATE_MID_ENEMY)
        # 自动创建大型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_BIG_ENEMY, consts.INTERVAL_OF_CREATE_BIG_ENEMY)
        # 自动创建子弹补给
        pygame.time.set_timer(consts.ID_OF_CREATE_BULLET_SUPPLY, consts.INTERVAL_OF_CREATE_BULLET_SUPPLY)

    @staticmethod
    def _stop_timers():
        # 停止自动发射子弹事件
        pygame.time.set_timer(consts.ID_OF_CREATE_BULLET, 0)
        # 停止自动创建小型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_SMALL_ENEMY, 0)
        # 停止自动创建中型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_MID_ENEMY, 0)
        # 停止自动创建大型敌机
        pygame.time.set_timer(consts.ID_OF_CREATE_BIG_ENEMY, 0)
        # 停止自动创建子弹补给
        pygame.time.set_timer(consts.ID_OF_CREATE_BULLET_SUPPLY, 0)
        # 停止自动发射双发子弹事件
        pygame.time.set_timer(consts.ID_OF_CREATE_DOUBLE_BULLET, 0)

    def run_game(self):
        # 让创建的窗口一直显示
        while True:
            # 处理事件
            self.handle_events()

            # 设置窗口背景颜色
            # self.window.fill(pygame.Color("lightskyblue"))

            if not self.is_game_over:
                # 检测碰撞
                self._check_collision()
            else:
                self._draw_game_over()

            self._draw_elements()

            # 将内存中的窗口对象绘制到屏幕上以更新屏幕
            pygame.display.flip()

            if not self.is_game_over and not self.pause_button.is_pause:
                # 更新背景
                self.bg.update()

                # 更新我方飞机位置
                self._update_position()

                # 删除窗口中不可见的元素
                self.delete_invisible_elements()

                # 切换图片
                self.switch_image()

            # 限定1s钟执行最大30次,即帧率
            self.clock.tick(consts.MAX_FRAMERATE)

    def switch_image(self):
        self.my_plane.switch_image()
        for bigEnemy in self.big_enemy_group.sprites():
            bigEnemy.switch_image()

    def _check_collision(self):
        """检测碰撞"""

        # 检测子弹与敌机的碰撞
        self._check_collision_bulletsordouble_small_enemy(self.bullet_group)
        self._check_collision_bulletsordouble_small_enemy(self.double_bullet_group)
        self._check_collision_bulletsordouble_mid_big_enemy(self.mid_enemy_group, self.bullet_group)
        self._check_collision_bulletsordouble_mid_big_enemy(self.mid_enemy_group, self.double_bullet_group)
        self._check_collision_bulletsordouble_mid_big_enemy(self.big_enemy_group, self.bullet_group)
        self._check_collision_bulletsordouble_mid_big_enemy(self.big_enemy_group, self.double_bullet_group)
        # 检测我方飞机和敌机的碰撞
        self._check_collision_myplane_enemy()
        # 检测我方飞机和双发子弹的碰撞
        self._check_collision_myplane_bulletsupply()
        # 检测我方飞机和炸弹的碰撞
        self._check_collision_myplane_bomb()

    def handle_events(self):
        """处理时间"""
        # 从时间队列中将所有时间全部取出并逐个进行处理
        for event in pygame.event.get():
            # 如果时间是退出程序
            if event.type == pygame.QUIT:
                if self.score_board.current_score > self.score_board.highest_score:
                    self.score_board.save_current_score()
                # 卸载pygame
                pygame.quit()
                # 退出程序
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._handle_up_events(event)
            elif event.type == consts.ID_OF_CREATE_BULLET:
                bullet = Bullet(self.window, self.my_plane)
                self.bullet_group.add(bullet)
            elif event.type == consts.ID_OF_CREATE_DOUBLE_BULLET:
                # 创建两颗双发子弹
                self._create_two_double_bullets()
            elif event.type == consts.ID_OF_CREATE_SMALL_ENEMY:
                small_enemy = SmallEnemy(self.window)
                self.small_enemy_group.add(small_enemy)
                self.enemy_group.add(small_enemy)
            elif event.type == consts.ID_OF_CREATE_MID_ENEMY:
                mid_enemy = MidEnemy(self.window)
                self.mid_enemy_group.add(mid_enemy)
                self.enemy_group.add(mid_enemy)
            elif event.type == consts.ID_OF_CREATE_BIG_ENEMY:
                big_enemy = BigEnemy(self.window)
                self.big_enemy_group.add(big_enemy)
                self.enemy_group.add(big_enemy)
                # 创建炸弹补给
                bomb_supply = BombSupply(self.window)
                self.bomb_group.add(bomb_supply)
            elif event.type == consts.ID_OF_CANCLE_INVINCIBLE:
                self.my_plane.is_invincible = False
                # 解除无敌状态事件
                pygame.time.set_timer(consts.ID_OF_CANCLE_INVINCIBLE, 0)
                pygame.time.set_timer(pygame.USEREVENT + 5, 0)
            elif event.type == consts.ID_OF_CANCLE_INVINCIBLE_CIRCLE_SPEED:
                if self.my_plane.is_invincible:
                    # self.circle_percentage -= 0.02
                    # 无敌护盾事件每次递减护盾百分比
                    self.circle_percentage -= consts.INTERVAL_OF_INVINCIBLE_CIRCLE_SPEED / consts.INTERVAL_OF_CANCLE_INVINCIBLE
            elif event.type == consts.ID_OF_CREATE_BULLET_SUPPLY:
                bullet_supply = BulletSupply(self.window)
                self.bullet_supply_group.add(bullet_supply)

    # 处理按键按下
    def _handle_keydown_events(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.my_plane.move_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.my_plane.move_down = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.my_plane.move_left = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.my_plane.move_right = True
        elif event.key == pygame.K_ESCAPE:
            if self.score_board.current_score > self.score_board.highest_score:
                self.score_board.save_current_score()
            # 卸载pygame
            pygame.quit()
            # 退出程序
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.is_game_over and self.visual_bomb_group.bomb_number > 0:
                # 发射一颗炸弹
                self._launch_bomb()
        elif event.key == pygame.K_p:
            if not self.is_game_over:
                self.pause_button.switch_image()
                self._handle_pause()
        elif event.key == pygame.K_r:
            self._handle_reset()

    # 处理按键抬起
    def _handle_up_events(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.my_plane.move_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.my_plane.move_down = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.my_plane.move_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.my_plane.move_right = False

    def _draw_elements(self):
        """绘制元素"""
        # 绘制背景
        self.my_plane.draw()
        # 在窗口中绘制所有子弹
        self.bullet_group.draw(self.window)
        # 在窗口中绘制双发子弹
        self.double_bullet_group.draw(self.window)
        # 在窗口中绘制所有子弹补给
        self.bullet_supply_group.draw(self.window)
        # 在窗口中绘制小型敌机
        self.small_enemy_group.draw(self.window)
        # 在窗口中绘制中型敌机
        self.mid_enemy_group.draw(self.window)
        # 在中型敌机尾部画上能量条
        for mid_enemy in self.mid_enemy_group.sprites():
            mid_enemy.draw_energy_lines()
        # 在窗口中绘制大型敌机
        self.big_enemy_group.draw(self.window)
        for big_enemy in self.big_enemy_group.sprites():
            big_enemy.draw_energy_lines()
        for i in range(self.my_plane.life_num):
            self.window.blit(self.my_plane.life_image, self.my_plane.life_rect_list[i])
        # 无敌护盾
        if self.my_plane.is_invincible:
            self.my_plane.draw_invincible(self.circle_percentage)
        # 绘制炸弹补给
        self.bomb_group.draw(self.window)
        # 在窗口绘制炸弹
        for i in range(self.visual_bomb_group.bomb_number):
            self.window.blit(self.visual_bomb_group.image, self.visual_bomb_group.bomb_rect_list[i])
        # 绘制分数
        self.score_board.draw_score()
        self.score_board.draw_highest_score()
        self.score_board.draw_current_level()
        self.window.blit(self.pause_button.image, self.pause_button.rect)

    def _update_position(self):
        """更新画面中的元素"""

        # 更新我方飞机位置
        self.my_plane.update()
        # 更新子弹位置
        self.bullet_group.update()
        # 更新双发子弹位置
        self.double_bullet_group.update()
        # 更新小型敌机位置
        self.small_enemy_group.update()
        # 更新小型敌机位置
        self.mid_enemy_group.update()
        # 更新小型敌机位置
        self.big_enemy_group.update()
        # 更新子弹补给位置
        self.bullet_supply_group.update()
        # 绘制炸弹补给
        self.bomb_group.update()

    def delete_invisible_elements(self):
        """删除窗口中不可见的元素"""

        # 删除窗口中不可见的子弹
        self.del_invisible_bullet(self.bullet_group)
        self.del_invisible_bullet(self.double_bullet_group)
        self.del_invisible_bullet(self.bomb_group)
        # 删除窗口中不可见的敌机

        self.del_invisible_element(self.enemy_group)
        self.del_invisible_element(self.bullet_supply_group)

    def del_invisible_bullet(self, group):
        """删除窗口中不可见的子弹"""

        for supply in group:
            if supply.rect.bottom <= 0:
                group.remove(supply)

    def del_invisible_element(self, group):
        """删除窗口中不可见的敌机/子弹补给"""

        for sprit in group.sprites():
            if sprit.rect.top > self.window.get_rect().height:
                # self.enemy_group.remove(enemy)
                # 将该架敌机从所有分组中删除
                sprit.kill()

    def _check_collision_bulletsordouble_small_enemy(self, group):
        """检测子弹或双发与小型敌机的碰撞"""

        # 检测碰撞
        dict_collided_enemy = pygame.sprite.groupcollide(self.small_enemy_group, group, False, True)
        # 如果小型敌机与子弹发生碰撞
        if len(dict_collided_enemy) > 0:
            for enemy in dict_collided_enemy.keys():
                if not enemy.explode_flag:
                    # 根据摧毁的敌机更新得分
                    self.update_current_score(enemy)
                    self.score_board.update_current_level()
                    self.update_enemy_supply_speed()
                    enemy.play_explode_sound()
                    # 标记敌机正在切换爆炸图片
                    enemy.explode_flag = True
        # 爆炸切换图片(如果将swich_explode_image和播放声音放在一起将无法起到爆炸切换计数器的效果)
        for enemy in self.small_enemy_group.sprites():
            # 如果某架敌机被标记为爆炸
            if enemy.explode_flag:
                # 切换敌机爆炸图片
                enemy.swich_explode_image()

    def _check_collision_bulletsordouble_mid_big_enemy(self, enemy_group, blt_group):
        """检测子弹与敌机的碰撞"""

        # 检测碰撞
        dict_collided_enemy = pygame.sprite.groupcollide(enemy_group, blt_group, False, True)
        # 如果敌机与子弹发生碰撞
        if len(dict_collided_enemy) > 0:
            for enemy in dict_collided_enemy.keys():
                if enemy.energy > 0:
                    # 如果与敌机发生碰撞的是子弹
                    if blt_group == self.bullet_group:
                        # 敌机能量减1
                        enemy.energy -= 1
                    # 如果与敌机发生碰撞的是双发子弹
                    elif blt_group == self.double_bullet_group:
                        # 如果与敌机发生碰撞的是1颗双发子弹
                        if len(dict_collided_enemy[enemy]) == 1:
                            # 敌机能量减1
                            enemy.energy -= 1
                        # 如果与敌机发生碰撞的是2颗双发子弹
                        elif len(dict_collided_enemy[enemy]) == 2:
                            # 敌机能量减2 如果能量变成-1则能量位置0
                            enemy.energy -= 2
                            if enemy.energy == -1:
                                enemy.energy = 0

                    # 每次击中能量减2

                # 能量为1爆炸
                if enemy.energy == 0:
                    if not enemy.explode_flag:
                        # 根据摧毁的敌机更新得分
                        self.update_current_score(enemy)
                        self.score_board.update_current_level()
                        self.update_enemy_supply_speed()
                        enemy.play_explode_sound()
                        # 标记敌机正在切换爆炸图片
                        enemy.explode_flag = True
                else:
                    if not enemy.hit_flag:
                        enemy.hit_flag = True

        # 爆炸切换图片(如果将swich_explode_image和播放声音放在一起将无法起到爆炸切换计数器的效果)
        for enemy in enemy_group.sprites():
            if enemy.hit_flag:
                enemy.swich_hit_image()
            # 如果某架敌机被标记为爆炸
            if enemy.explode_flag:
                # 切换敌机爆炸图片
                enemy.swich_explode_image()

    def _check_collision_myplane_enemy(self):
        """我方飞机和敌机碰撞"""

        # 可见部分碰撞 (pygame.sprite.collide_mask)
        list_collided = pygame.sprite.spritecollide(self.my_plane, self.enemy_group, False, pygame.sprite.collide_mask)
        # 如果发生碰撞
        if len(list_collided) > 0:
            if not self.my_plane.is_invincible:
                # 发生碰撞生命减1
                self.my_plane.life_num -= 1
                self.my_plane.play_explode_sound()

                # 如果生命数>0 重置我方飞机位置
                if self.my_plane.life_num > 0:
                    self.my_plane.reset_position()
                    # 标记我方飞机出于无敌状态
                    self.my_plane.is_invincible = True
                    # 无敌护盾圆百分比
                    self.circle_percentage = 1
                    # 在事件队列中每隔一段时间就解除无敌状态
                    pygame.time.set_timer(consts.ID_OF_CANCLE_INVINCIBLE, consts.INTERVAL_OF_CANCLE_INVINCIBLE)
                    pygame.time.set_timer(consts.ID_OF_CANCLE_INVINCIBLE_CIRCLE_SPEED,
                                          consts.INTERVAL_OF_INVINCIBLE_CIRCLE_SPEED)
                    # 在事件队列中停止生成自定义事件"创建双发子弹"
                    pygame.time.set_timer(consts.ID_OF_CREATE_DOUBLE_BULLET, 0)
                    # 在事件队列中每隔一段时间就生成一个自定义事件"创建子弹"
                    pygame.time.set_timer(consts.ID_OF_CREATE_BULLET,
                                          consts.INTERVAL_OF_CREATE_BULLET)
                else:
                    self.is_game_over = True
                    # 定时定时器
                    self._stop_timers()
                    # 停止播放背景音乐
                    pygame.mixer.music.stop()

                for enemy in list_collided:
                    if not enemy.explode_flag:
                        self.update_current_score(enemy)
                        self.score_board.update_current_level()
                        self.update_enemy_supply_speed()
                        enemy.play_explode_sound()
                        # 标记敌机正在切换爆炸图片
                        enemy.explode_flag = True
        for enemy in self.enemy_group.sprites():
            # 如果某架敌机被标记为爆炸
            if enemy.explode_flag:
                # 切换敌机爆炸图片
                enemy.swich_explode_image()

    def _create_two_double_bullets(self):
        """创建两颗双发子弹"""

        # 双发子弹的计数器加1
        self.double_bullet_counter += 1

        # 如果双发子弹计数器的值没有达到最大值
        if self.double_bullet_counter != consts.DOUBLE_BULLET_COUNTER_MAX:
            # 创建一颗位于我方飞机左翼的双发子弹
            double_bullet1 = DoubleBullet(self.window, self.my_plane)

            # 设置我方飞机左翼的双发子弹的初始位置
            double_bullet1.rect.center = (self.my_plane.rect.centerx -
                                          consts.DOUBLE_BULLET_OFFSET,
                                          self.my_plane.rect.centery)

            # 创建一颗位于我方飞机右翼的双发子弹
            double_bullet2 = DoubleBullet(self.window, self.my_plane)

            # 设置我方飞机右翼的双发子弹的初始位置
            double_bullet2.rect.center = (self.my_plane.rect.centerx +
                                          consts.DOUBLE_BULLET_OFFSET,
                                          self.my_plane.rect.centery)

            # 将创建的两颗双发子弹添加到管理所有双发子弹的分组中
            self.double_bullet_group.add(double_bullet1)
            self.double_bullet_group.add(double_bullet2)
        # 如果双发子弹计数器的值达到最大值
        else:
            # 在事件队列中每隔一段时间就生成一个自定义事件"创建子弹"
            pygame.time.set_timer(consts.ID_OF_CREATE_BULLET,
                                  consts.INTERVAL_OF_CREATE_BULLET)

            # 在事件队列中停止生成自定义事件"创建双发子弹"
            pygame.time.set_timer(consts.ID_OF_CREATE_DOUBLE_BULLET, 0)

            # 双发子弹的计数器重置为0
            self.double_bullet_counter = 0

    def _check_collision_myplane_bulletsupply(self):
        """检测我方飞机和双发子弹碰撞"""
        # 可见部分碰撞 (pygame.sprite.collide_mask)
        list_collided = pygame.sprite.spritecollide(self.my_plane, self.bullet_supply_group, False,
                                                    pygame.sprite.collide_mask)
        # 如果发生碰撞
        if len(list_collided) > 0:
            for bullet_supply in list_collided:
                bullet_supply.play_collide_sound()
                # 将子弹补给从管理它的所有分组中删除
                bullet_supply.kill()
            # 在事件队列中停止生成自定义事件"创建子弹"
            pygame.time.set_timer(consts.ID_OF_CREATE_BULLET, 0)

            # 在事件队列中每隔一段时间就生成一个自定义事件"创建双发子弹"
            pygame.time.set_timer(consts.ID_OF_CREATE_DOUBLE_BULLET,
                                  consts.INTERVAL_OF_CREATE_DOUBLE_BULLET)

            # 双发子弹的计数器重置为0
            self.double_bullet_counter = 0

    def _check_collision_myplane_bomb(self):
        """检测我方飞机和炸弹碰撞"""

        # 可见部分碰撞 (pygame.sprite.collide_mask)
        list_collided = pygame.sprite.spritecollide(self.my_plane, self.bomb_group, False,
                                                    pygame.sprite.collide_mask)
        # 如果发生碰撞
        if len(list_collided) > 0:
            for bomb_supply in list_collided:
                bomb_supply.play_collide_sound()
                # 将炸弹补给从管理它的所有分组中删除
                bomb_supply.kill()
                # 炸弹数小于3才补给
                if self.visual_bomb_group.bomb_number < 3:
                    self.visual_bomb_group.bomb_number += 1

    def _draw_game_over(self):
        """绘制游戏结束文本"""

        text = '游戏结束'
        prompt_text_surface = self.font_36.render(text, True, consts.WHITE_COLOR)
        prompt_text_surface_rect = prompt_text_surface.get_rect()
        prompt_text_surface_rect.center = self.window.get_rect().center
        self.window.blit(prompt_text_surface, prompt_text_surface_rect)

    def _launch_bomb(self):
        """发射一颗炸弹"""
        # 播放炸弹播放的声音
        self.visual_bomb_group.play_explode_sound()
        # 销毁画面中的敌机
        for enemy in self.enemy_group.sprites():
            # 根据摧毁的敌机更新得分
            self.update_current_score(enemy)
            self.score_board.update_current_level()
            self.update_enemy_supply_speed()
            # 将敌机从所有敌机分组中删除
            enemy.kill()
        # 炸弹数量减1
        self.visual_bomb_group.bomb_number -= 1

    def update_current_score(self, enemy):
        """更新得分"""
        if type(enemy) == SmallEnemy:
            self.score_board.current_score += consts.SCORE_SMALL_ENEMY
        elif type(enemy) == MidEnemy:
            self.score_board.current_score += consts.SCORE_MID_ENEMY
        if type(enemy) == BigEnemy:
            self.score_board.current_score += consts.SCORE_BIG_ENEMY

    def update_enemy_supply_speed(self):
        """根据当前关数更新所有敌机和补给的速度"""
        if len(self.score_board.speed_flag) > 0 and self.score_board.speed_flag[self.score_board.current_level - 1]:
            pixels = self.score_board.current_level / 10
            SmallEnemy.update_offset(pixels)
            MidEnemy.update_offset(pixels)
            BigEnemy.update_offset(pixels)
            BulletSupply.update_offset(pixels)
            BombSupply.update_offset(pixels)
            # 速度加完再把标记为复原
            self.score_board.speed_flag[self.score_board.current_level - 1] = False
            # print("第",self.score_board.current_level,"关",SmallEnemy.offset)

    def _play_bg_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/bgm.ogg')
        pygame.mixer.music.set_volume(consts.BG_SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    def _handle_pause(self):
        # 游戏处于暂停状态

        if self.pause_button.is_pause:
            # 暂停播放爆炸或碰撞的声音文件
            pygame.mixer.pause()
            # 暂停播放背景音乐的声音文件
            pygame.mixer.music.pause()
            # 停止定时器
            self._stop_timers()
        # 游戏不处于暂停状态
        else:
            # 继续播放爆炸或碰撞的声音文件
            pygame.mixer.unpause()
            # 继续播放背景音乐的声音文件
            pygame.mixer.music.unpause()
            # 设置定时器
            self._set_timers()

    def _handle_reset(self):
        """处理鼠标对重新开始游戏的单击"""

        self._stop_timers()

        # 重新循环播放背景音乐
        pygame.mixer.music.play(-1)

        # 重置我方飞机的位置
        self.my_plane.reset_position()
        # 重置我方飞机的初始生命数
        self.my_plane.life_number = consts.LIFE_NUM

        # 重置炸弹的初始数量
        self.visual_bomb_group.bomb_number = consts.BOMB_INITIAL_NUMBER

        # 如果当前得分大于最高得分
        if self.score_board.current_score > self.score_board.highest_score:
            # 将当前得分作为最高得分保存到文件
            self.score_board.save_current_score()
            # 将当前得分作为最高得分赋值给实例属性highest_score
            self.score_board.highest_score = self.score_board.current_score

        # 重置当前分数
        self.score_board.current_score = 0
        # 重置当前关数
        self.score_board.current_level = 1

        # 删除所有分组中的所有精灵
        self._empty_all_groups()

        # 设置定时器

        self._set_timers()

        # 标记游戏没有结束
        self.is_game_over = False

        # 重置双发子弹的计数器
        self.double_bullet_counter = 0

        # 重置所有的实例属性
        self._reset_offsets()

    def _empty_all_groups(self):
        """删除所有分组中的所有精灵"""

        # 删除子弹分组中的所有精灵
        self.bullet_group.empty()

        # 删除双发子弹分组中的所有精灵
        self.double_bullet_group.empty()

        # 删除子弹补给分组中的所有精灵
        self.bullet_supply_group.empty()

        # 删除炸弹补给分组中的所有精灵
        self.bomb_group.empty()

        # 删除小型敌机分组中的所有精灵
        self.small_enemy_group.empty()

        # 删除中型敌机分组中的所有精灵
        self.mid_enemy_group.empty()

        # 删除大型敌机分组中的所有精灵
        self.big_enemy_group.empty()

        # 删除所有子弹分组中的所有精灵
        self.enemy_group.empty()

    def _reset_offsets(self):
        """重置敌机和供给每次移动时的偏移量"""

        # 重置小型敌机每次移动时的偏移量
        SmallEnemy.offset = consts.SMALL_ENEMY_OFFSET

        # 重置中型敌机每次移动时的偏移量
        MidEnemy.offset = consts.MID_ENEMY_OFFSET

        # 重置大型敌机每次移动时的偏移量
        BigEnemy.offset = consts.BIG_ENEMY_OFFSET

        # 重置子弹补给每次移动时的偏移量
        BulletSupply.offset = consts.BULLET_SUPPLY_OFFSET

        # 重置炸弹补给每次移动时的偏移量
        BombSupply.offset = consts.BOMB_SUPPLY_OFFSET


if __name__ == '__main__':
    PlaneWar().run_game()
