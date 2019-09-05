# available on Windows

from pynput.keyboard import Key, Controller
from cuser import SerAction
import time

def next(k):
    k[0].press(Key.right)
    k[0].release(Key.right)

def pre(k):
    k[0].press(Key.left)
    k[0].release(Key.left)



k = Controller()
s = SerAction()

s.connection()
s.listen_load('key1', next, [k])
s.listen_load('key2', pre, [k])
t = 0


while True:
    time.sleep(1)
    t += 1
    s.set_nixie(str(t))