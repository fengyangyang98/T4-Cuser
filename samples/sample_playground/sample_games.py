from turtle import *
from random import randrange
from freegames import square, vector, floor
from cuser import SerAction
from random import *
import time

"""Snake, classic arcade game.

Excercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""


class Snacke():
    def __init__(self, page_number, page_update, page_back, ser):
        self.food = vector(0, 0)
        self.snake = [vector(10, 0)]
        self.aim = vector(0, -10)

        self.page_number = page_number
        self.page_now = 0

        self.best = 0

        self.page_update = page_update
        self.page_back = page_back
        self.ser = ser

    def __write_words(self, words, x, y, size, style, the_color, postion):
        penup()
        goto(x, y)
        pendown()
        color((0, 0, 0), the_color)
        write(words, font=("Arial", size, style), align=postion)

    def init(self):
        clear()
        hideturtle()
        tracer(False)
        self.best = self.ser.read_mem(self.page_number)
        self.ser.set_nixie(str(self.best).zfill(3) + '  ' + str(len(self.snake)).zfill(3))
        self.__write_words("Best Score: " + str(self.best), 0, 0, 30, "bold", "black", "center")
        time.sleep(1)
        update()

    def change(self, ax):
        "Change snake direction."
        self.aim.x = ax[0]
        self.aim.y = ax[1]

    def inside(self, head):
        "Return True if head inside boundaries."
        return -200 < head.x < 190 and -200 < head.y < 190

    def move(self):
        "Move snake forward one segment."

        if self.page_number != self.page_now:
            return

        head = self.snake[-1].copy()
        head.move(self.aim)

        # die
        if not self.inside(head) or head in self.snake:
            square(head.x, head.y, 9, 'red')
            update()

            if len(self.snake) > self.best:
                self.__write_words("Best Score: " + str(len(self.snake)) + " !", 0, 0, 30, "bold", 'black', "center")
                self.__write_words("Best Score: " + str(len(self.snake)) + " !", 0, 0, 30, "bold", 'black', "center")
                self.ser.write_mem(self.page_number, len(self.snake))
            else:
                self.__write_words("GAME OVER!", 0, 0, 30, "bold", 'black', "center")

            self.ser.buzzer_start()
            time.sleep(2)
            self.ser.buzzer_stop()
            self.page_update([self.page_back])
            return

        self.snake.append(head)

        if head == self.food:
            self.food.x = randrange(-15, 15) * 10
            self.food.y = randrange(-15, 15) * 10
        else:
            self.snake.pop(0)

        clear()

        for body in self.snake:
            square(body.x, body.y, 9, 'black')

        square(self.food.x, self.food.y, 9, 'green')

        # update the nixie
        self.ser.set_nixie(str(max(self.best, len(self.snake))).zfill(3) + '  ' + str(len(self.snake)).zfill(3))

        update()
        ontimer(self.move, 80)


"""Flappy, game inspired by Flappy Bird.

Exercises

1. Keep score.
2. Vary the speed.
3. Vary the size of the balls.
4. Allow the bird to move forward and back.

"""


class Flappy():
    def __init__(self, page_number, page_update, page_back, ser):
        self.bird = vector(0, 0)
        self.balls = []

        self.page_number = page_number
        self.page_now = 0

        self.best = 0

        self.page_update = page_update
        self.page_back = page_back
        self.ser = ser
        self.score = 0

    def __write_words(self, words, x, y, size, style, the_color, postion):
        penup()
        goto(x, y)
        pendown()
        color((0, 0, 0), the_color)
        write(words, font=("Arial", size, style), align=postion)

    def init(self):
        clear()

        self.best = self.ser.read_mem(self.page_number)
        self.ser.set_nixie(str(self.best).zfill(3) + '  ' + str(self.score).zfill(3))
        self.__write_words("Best Score: " + str(self.best), 0, 0, 30, "bold", "black", "center")

        up()
        hideturtle()
        listen()
        tracer(False)

        time.sleep(1)
        update()

    def tap(self, empty):
        "Move bird up in response to screen tap."
        up = vector(0, 10)
        self.bird.move(up)

    def inside(self, point):
        "Return True if point on screen."
        return -200 < point.x < 200 and -200 < point.y < 200

    def draw(self, alive):
        "Draw screen objects."
        clear()
        hideturtle()
        goto(self.bird.x, self.bird.y)

        if alive:
            dot(10, 'green')
        else:
            dot(10, 'red')

        for ball in self.balls:
            goto(ball.x, ball.y)
            dot(20, 'black')

        # update()

    def move(self):
        "Update object positions."

        if self.page_number != self.page_now:
            return

        die = 0
        self.bird.y -= 5

        for ball in self.balls:
            ball.x -= 3

        if randrange(10) == 0:
            y = randrange(-199, 199)
            ball = vector(199, y)
            self.balls.append(ball)

        while len(self.balls) > 0 and not self.inside(self.balls[0]):
            self.balls.pop(0)
            self.score += 1

        if not self.inside(self.bird):
            self.draw(False)
            die = 1

        for ball in self.balls:
            if abs(ball - self.bird) < 15:
                self.draw(False)
                die = 1

        if die == 1:
            if self.score > self.best:
                self.__write_words("Best Score: " + str(self.score) + " !", 0, 0, 30, "bold", 'black', "center")
                self.__write_words("Best Score: " + str(self.score) + " !", 0, 0, 30, "bold", 'black', "center")
                self.ser.write_mem(self.page_number, self.score)
            else:
                self.__write_words("GAME OVER!", 0, 0, 30, "bold", 'black', "center")

            time.sleep(3)
            self.page_update([self.page_back])
            return

        self.ser.set_nixie(str(max(self.score, self.best)).zfill(3) + '  ' + str(self.score).zfill(3))
        self.draw(True)

        ontimer(self.move, 80)


"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""


class Pacman():
    def __init__(self, page_number, page_update, page_back, ser):
        self.state = {'score': 0}
        self.path = Turtle(visible=False)
        self.writer = Turtle(visible=False)
        self.aim = vector(5, 0)
        self.pacman = vector(-40, -80)
        self.ghosts = [
            [vector(-180, 160), vector(5, 0)],
            [vector(-180, -160), vector(0, 5)],
            [vector(100, 160), vector(0, -5)],
            [vector(100, -160), vector(-5, 0)],
        ]

        self.tiles = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
            0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

        self.page_number = page_number
        self.page_now = 0

        self.best = 0

        self.page_update = page_update
        self.page_back = page_back
        self.ser = ser

    def __write_words(self, words, x, y, size, style, the_color, postion):
        penup()
        goto(x, y)
        pendown()
        color((0, 0, 0), the_color)
        write(words, font=("Arial", size, style), align=postion)

    def init(self):
        clear()
        hideturtle()
        tracer(False)
        self.best = self.ser.read_mem(self.page_number)
        self.ser.set_nixie(str(self.best).zfill(3) + '  ' + str(self.state['score']).zfill(3))
        self.__write_words("Best Score: " + str(self.best), 0, 0, 30, "bold", "black", "center")
        time.sleep(1)

        hideturtle()
        tracer(False)
        self.writer.goto(160, 160)
        self.writer.color('white')
        self.writer.write(self.state['score'])

        self.world()
    def square(self, x, y):
        "Draw square using path at (x, y)."
        self.path.up()
        self.path.goto(x, y)
        self.path.down()
        self.path.begin_fill()

        for count in range(4):
            self.path.forward(20)
            self.path.left(90)

        self.path.end_fill()

    def offset(self, point):
        "Return offset of point in tiles."
        x = (floor(point.x, 20) + 200) / 20
        y = (180 - floor(point.y, 20)) / 20
        index = int(x + y * 20)
        return index

    def valid(self, point):
        "Return True if point is valid in tiles."
        index = self.offset(point)

        if self.tiles[index] == 0:
            return False

        index = self.offset(point + 19)

        if self.tiles[index] == 0:
            return False

        return point.x % 20 == 0 or point.y % 20 == 0

    def world(self):
        "Draw world using path."
        self.path.speed(10)
        self.writer.speed(10)
        bgcolor('black')
        self.path.color('blue')

        for index in range(len(self.tiles)):
            tile = self.tiles[index]

            if tile > 0:
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                self.square(x, y)

                if tile == 1:
                    self.path.up()
                    self.path.goto(x + 10, y + 10)
                    self.path.dot(2, 'white')


    def move(self):
        "Move pacman and all ghosts."

        if self.page_number != self.page_now:
            return

        self.writer.undo()
        self.writer.write(self.state['score'])

        clear()

        if self.valid(self.pacman + self.aim):
            self.pacman.move(self.aim)

        index = self.offset(self.pacman)

        if self.tiles[index] == 1:
            self.tiles[index] = 2
            self.state['score'] += 1
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            self.square(x, y)

        up()
        goto(self.pacman.x + 10, self.pacman.y + 10)
        dot(20, 'yellow')

        for point, course in self.ghosts:
            if self.valid(point + course):
                point.move(course)
            else:
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y

            up()
            goto(point.x + 10, point.y + 10)
            dot(20, 'red')

        update()

        for point, course in self.ghosts:
            if abs(self.pacman - point) < 20:
                if self.state['score'] > self.best:
                    self.__write_words("Best Score: " + str(self.state['score']) + " !", 0, 0, 30, "bold", 'white',
                                       "center")
                    self.__write_words("Best Score: " + str(self.state['score']) + " !", 0, 0, 30, "bold", 'white',
                                       "center")
                    self.ser.write_mem(self.page_number, self.state['score'])
                else:
                    self.__write_words("GAME OVER!", 0, 0, 30, "bold", 'white', "center")

                time.sleep(3)
                self.path.clear()
                self.writer.clear()
                bgcolor('white')

                self.page_update([self.page_back])
                return

        # update the nixie
        self.ser.set_nixie(str(max(self.best, self.state['score'])).zfill(3) + '  ' + str(self.state['score']).zfill(3))

        ontimer(self.move, 70)

    def change(self, axi):
        "Change pacman aim if valid."
        if self.valid(self.pacman + vector(axi[0], axi[1])):
            self.aim.x = axi[0]
            self.aim.y = axi[1]
