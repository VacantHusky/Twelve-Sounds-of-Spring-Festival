# -*- coding: UTF-8 –*-

# Twelve-of-Spring-Festival
# 春节十二响
# Author: WangHu
# Mail:   wanghu10158@gmail.com
# Last Updated: 2019-08-14
#
# 模拟烟花

import pygame, math, time, random, os
from sys import exit

WINDOW_W = 940
WINDOW_H = 620
one_time = 0.18 #时间流速
show_n = 0
show_frequency = 0.0015 #烟花绽放频率，数值越大频率越高
color_list = [
    [255, 50, 50],
    [50, 255, 50],
    [50, 50, 255],
    [255, 255, 50],
    [255, 50, 255],
    [50, 255, 255],
    [255, 255, 255]
]

# 初始化pygame
pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150,50)
# 创建一个窗口
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("烟花")
sound_wav = pygame.mixer.music.load("yanhua.mp3")
pygame.mixer.music.play()
class Yanhua():
    is_show = False
    x, y = 0, 0
    vy = 0
    p_list = []
    color = [0, 0, 0]
    v = 0

    def __init__(self, x, y, vy, n=300, color=[0, 255, 0], v=10):
        self.x = x
        self.y = y
        self.vy = vy
        self.color = color
        self.v = v
        # self.is_show = True
        for i in range(n):
            self.p_list.append([random.random() * 2 * math.pi, 0, v * math.pow(random.random(), 1 / 3)])

    def chongzhi(self):
        self.is_show = True
        self.x = random.randint(WINDOW_W // 2 - 350, WINDOW_W // 2 + 350)
        self.y = random.randint(int(WINDOW_H / 2), int(WINDOW_H * 3 / 5))
        self.vy = -40 * (random.random() * 0.4 + 0.8) - self.vy * 0.2
        self.color = color_list[random.randint(0, len(color_list) - 1)].copy()
        n = len(self.p_list)
        self.p_list = []
        for i in range(n):
            self.p_list.append([random.random() * 2 * math.pi, 0, self.v * math.pow(random.random(), 1 / 3)])

    def run(self):
        global show_n
        for p in self.p_list:
            p[1] = p[1] + (random.random() * 0.6 + 0.7) * p[2]
            p[2] = p[2] * 0.97
            if p[2] < 1.2:
                self.color[0] *= 0.9999
                self.color[1] *= 0.9999
                self.color[2] *= 0.9999

            if max(self.color) < 10 or self.y>WINDOW_H+p[1]:
                show_n -= 1
                self.is_show = False
                break
        self.vy += 10 * one_time
        self.y += self.vy * one_time


yh_list = []
yh_list.append(Yanhua(300, 300, -20, n=100, color=[0, 255, 0], v=10))
yh_list.append(Yanhua(300, 300, -20, n=200, color=[0, 0, 255], v=11))
yh_list.append(Yanhua(300, 300, -20, n=200, color=[0, 0, 255], v=12))
yh_list.append(Yanhua(300, 300, -20, n=500, color=[0, 0, 255], v=12))
yh_list.append(Yanhua(300, 300, -20, n=600, color=[0, 0, 255], v=13))
yh_list.append(Yanhua(300, 300, -20, n=700, color=[255, 0, 0], v=15))
yh_list.append(Yanhua(300, 300, -20, n=800, color=[255, 255, 0], v=18))

clock = pygame.time.Clock()
# 游戏主循环
while True:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 接收到退出时间后退出程序
            exit()

    # 将背景图画上去
    screen.fill((0, 0, 0))
    # 放烟花
    for i, yh in enumerate(yh_list):
        if not yh.is_show:
            yh.is_show = False
            if random.random() < show_frequency * (len(yh_list) - show_n):
                show_n += 1
                yh.chongzhi()
            continue
        yh.run()
        for p in yh.p_list:
            x, y = yh.x + p[1] * math.cos(p[0]), yh.y + p[1] * math.sin(p[0])
            if random.random() < 0.055:
                screen.set_at((int(x), int(y)),(255,255,255))
            else:
                screen.set_at((int(x), int(y)), (int(yh.color[0]), int(yh.color[1]), int(yh.color[2])))

    # 刷新画面
    pygame.display.update()
    # 返回上一个调用的时间（ms）
    time_passed = clock.tick(50)
