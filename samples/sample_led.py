from cuser import SerAction
import time
def hello(ser):
    ser[0].set_nixie('abcd')

def play(nixie, led, ser):
    i = 0
    while(True):
        i = (i+ 1) % 4
        ser.set_nixie(nixie[i])
        ser.set_led(led[i])
        time.sleep(0.5)


nixie = [
    '1      8',
    ' 2    7 ',
    '  3  6  ',
    '   45  '
]

led = [0x81, 0x42, 0x24, 0x18]

ser = SerAction()
ser.connection()
play(nixie, led, ser)