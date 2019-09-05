from cuser import SerAction
import time


def led(s):
    number = 1
    print(111)
    while number <= 128:
        s[0].set_led(number)
        number = number * 2
        time.sleep(0.1)

    s[0].set_led(0)


s = SerAction()
s.connection()
s.listen_load('vibrate', led, [s])
s.vibrate_start()
s.set_nixie('       ')
s.set_led(0)
