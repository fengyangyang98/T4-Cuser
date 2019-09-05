from turtle import *
from cuser import SerAction


class ConnectingPage():
    def __init__(self, page_number):
        self.num = 0
        self.page_now = -1
        self.page_number = page_number

    def write_words(self, words, x, y):
        penup()
        goto(x, y)
        pendown()
        write(words, font=("Arial", 24, "normal"), align="center")
        penup()

    def page_animation(self):

        if self.page_now == self.page_number:
            clear()
            self.write_words("Welcome to the Game!", 0, 50)
            if self.num == 0:
                self.write_words("Connecting to the device.", 0, 20)
            elif self.num == 1:
                self.write_words("Connecting to the device..", 0, 20)
            elif self.num == 2:
                self.write_words("Connecting to the device...", 0, 20)

            self.num += 1
            if self.num == 3:
                self.num = 0

            ontimer(self.page_animation, 1000)
        else:
            pass


class ChoosePage():
    def __init__(self, page_number, page_update):
        self.item_number = 3
        self.ditance = [30, -10, -50]
        self.item_list = ["Snack", "Flappy", "Pacman"]
        self.choose_now = 0
        self.chosen_item = 0

        self.page_now = -1
        self.page_number = page_number

        self.page_update = page_update

    def init(self):
        clear()
        hideturtle()
        tracer(False)
        color((0, 0, 0), "black")
        self.chosen_item = 0
        self.write_words("Choose the Game:", 0, 80, "normal")

    def write_words(self, words, x, y, type):
        penup()
        goto(x, y)
        pendown()
        write(words, font=("Arial", 24, type), align="center")
        penup()

    def change(self, number):
        clear()
        self.choose_now += number[0]
        if self.choose_now < 0:
            self.choose_now = 0
        elif self.choose_now > self.item_number - 1:
            self.choose_now = self.item_number - 1
        self.chosen_item = self.choose_now + 2



    def move(self):
        self.write_words("Choose the Game:", 0, 80, "normal")
        for i in range(0, self.item_number):
            if i == self.choose_now:
                self.write_words(self.item_list[i], 0, self.ditance[i], "bold")
            self.write_words(self.item_list[i], 0, self.ditance[i], "normal")

        if self.page_now == self.page_number:
            ontimer(self.move, 100)

    def enter(self, empty):

        self.page_update([self.chosen_item])
