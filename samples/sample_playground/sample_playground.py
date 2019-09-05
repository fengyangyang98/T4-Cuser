from cuser import SerAction
from sample_homepage import ConnectingPage, ChoosePage
from sample_games import Snacke, Flappy, Pacman
from turtle import *
import time


class Playground():
    def __init__(self):
        self.page_now = 0

        self.ser = SerAction()

        self.page_back = 1

        self.connecting_page = ConnectingPage(0)
        self.choose_page = ChoosePage(1, self.__page_update)
        self.snack_page = Snacke(2, self.__page_update, self.page_back, self.ser)
        self.flappy_page = Flappy(3, self.__page_update, self.page_back, self.ser)
        self.pacman_page = Pacman(4, self.__page_update, self.page_back, self.ser)

        self.__setting()
        self.__page_update([self.page_now])
        self.page_switch()

        done()

    def __setting(self):
        pensize(4)
        tracer(False)
        up()
        hideturtle()
        colormode(255)
        color((0, 0, 0), "black")
        setup(420, 420, 370, 0)

    def __page_update(self, page):
        self.page_now = page[0]
        self.connecting_page.page_now = self.page_now
        self.choose_page.page_now = self.page_now
        self.snack_page.page_now = self.page_now
        self.flappy_page.page_now = self.page_now
        self.pacman_page.page_now = self.page_now

        self.ser.listen_unload('key1')
        self.ser.listen_unload('key2')
        self.ser.listen_unload('key3')
        self.ser.listen_unload('up')
        self.ser.listen_unload('down')
        self.ser.listen_unload('left')
        self.ser.listen_unload('right')
        self.ser.listen_unload('enter')
        time.sleep(0.2)

        self.page_switch()

    def page_switch(self):
        if self.page_now == 0:
            self.connecting_page.page_animation()
            self.ser.connection()
            self.page_now = 1
            self.__page_update([self.page_now])

        elif self.page_now == 1:
            self.ser.listen_load('up', self.choose_page.change, [-1])
            self.ser.listen_load('down', self.choose_page.change, [1])
            self.ser.listen_load('enter', self.choose_page.enter, [])
            self.ser.set_nixie('choosing')
            self.choose_page.init()
            self.choose_page.move()

        elif self.page_now == 2:
            self.ser.listen_load('right', self.snack_page.change, [10, 0])
            self.ser.listen_load('left', self.snack_page.change, [-10, 0])
            self.ser.listen_load('up', self.snack_page.change, [0, 10])
            self.ser.listen_load('down', self.snack_page.change, [0, -10])
            self.snack_page.init()
            self.snack_page.move()

        elif self.page_now == 3:
            self.ser.listen_load('key1', self.flappy_page.tap, [])
            self.flappy_page.init()
            self.flappy_page.move()

        elif self.page_now == 4:
            self.ser.listen_load('right', self.pacman_page.change, [5, 0])
            self.ser.listen_load('left', self.pacman_page.change, [-5, 0])
            self.ser.listen_load('up', self.pacman_page.change, [0, 5])
            self.ser.listen_load('down', self.pacman_page.change, [0, -5])
            self.pacman_page.init()
            self.pacman_page.move()



a = Playground()