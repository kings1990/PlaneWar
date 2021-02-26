"""测试矩形的属性"""

import pygame

rect = pygame.Rect(100, 50, 180, 120)


print("left =", rect.left)
print("top =", rect.top)
print("width =", rect.width)
print("height =", rect.height)
# right = left + width
print("right =", rect.right)
# bottom = top + height
print("bottom =", rect.bottom)
# centerx = left + width / 2
print("centerx =", rect.centerx)
# centery = top + height / 2
print("centery =", rect.centery)

# x = left
print("x =", rect.x)
# y = top
print("y =", rect.y)
# w = width
print("w =", rect.w)
# h = height
print("h =", rect.h)

# size = (width, height)
print("size =", rect.size)
# center = (centerx, centery)
print("center =", rect.center)

# topleft = (left, top)，左上角
print("topleft =", rect.topleft)
# bottomleft = (left, bottom), 左下角
print("bottomleft =", rect.bottomleft)
# bottomright = (right, bottom), 右下角
print("bottomright =", rect.bottomright)
# topright = (right, top)，右上角
print("topright =", rect.topright)

# midtop = (centerx, top), 上边缘中心点
print("midtop =", rect.midtop)
# midleft = (left, centery)，左边缘中心点
print("midleft =", rect.midleft)
# midbottom = (centerx, bottom)，下边缘中心点
print("midbottom =", rect.midbottom)
# midright = (right, centery)，右边缘中心点
print("midright =", rect.midright)

# rect.width = 170
# rect.w = 170
rect.size = (170, rect.height)
print(rect.width)
