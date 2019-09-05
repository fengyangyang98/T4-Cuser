from cuser import SerAction
import time

def hello(ser):
    print(ser[0].get_485_buffer())

def hi(ser):
    print(ser[0].send_485(0x20))



ser = SerAction()
ser.connection()

ser.listen_load('key1', hello, [ser])
ser.listen_load('key2', hi, [ser])



