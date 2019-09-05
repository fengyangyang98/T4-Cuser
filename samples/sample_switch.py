from cuser import SerAction
from pynput.keyboard import Key, Controller

def press_and_release(k):
    k[0].press(k[1])
    k[0].release(k[1])

k = Controller()
s = SerAction()

s.connection()
s.listen_load('up', press_and_release, [k, Key.up])
s.listen_load('down', press_and_release, [k, Key.down])
s.listen_load('left', press_and_release, [k, Key.left])
s.listen_load('right', press_and_release, [k, Key.right])
s.listen_load('key2', press_and_release, [k, Key.space])