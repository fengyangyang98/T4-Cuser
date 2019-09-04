#coding:utf-8

# MIT License
#
# Copyright (c) 2019 The Cuser
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software
# and associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the
# following conditions:
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import serial.tools.list_ports
from threading import Timer
import time


# Basic function:
# don't recommend the developer use the function below:
#
# port_check: get the list of the serial
# port_open: open the serial that
# port_close: close the serial
# port_send: send a char to the buffer
# port_send_list: send a bunch of chars to the bufffer
# port_receive: receive a list of chars

class BasicSerAction():
    def __init__(self):

        # Initialize the ser setting
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'

    # port_check:
    # Argument:
    # Return: list of the ports

    def port_check(self):

        return list(serial.tools.list_ports.comports())

    # port_open:
    # Argument: port: port to be opened
    # Return: 0 for failure, 1 for success

    def port_open(self, port):
        try:
            self.ser.port = port
            if self.ser.isOpen():
                self.ser.close()
            self.ser.open()
            return 1
        except:
            return 0

    # port_close:
    # Argument:
    # Return: 0 for failure, 1 for success

    def port_close(self):
        try:
            if self.ser.isOpen():
                self.ser.close()
            return 1
        except:
            return 0

    # port_send:
    # Argument: data(a char to send)
    # Return: 0 for failure, 1 for success

    def port_send(self, data):
        if self.ser.isOpen():
            send_list = []
            send_list.append(data)
            input_s = bytes(send_list)
            self.ser.write(input_s)
            return 1
        else:
            return 0

    # port_send_list:
    # Argument: a list of chars to send
    # Return: 0 for failure, 1 for success

    def port_send_list(self, datalist):
        if self.ser.isOpen():
            input_s = bytes(datalist)
            self.ser.write(input_s)
            return 1
        else:
            return 0

    # port_receive
    # Argument:
    # Return: a list of data received

    def port_receive(self):
        try:
            num = self.ser.inWaiting()
            if num > 0:
                data = self.ser.read(num)
                datalist = []
                for i in range(0, num):
                    datalist.append(data[i])

                return datalist

        except:
            return []


# serial function:
# provide the user the interface to use the serial
#
# connection: connect the serial
# disconnection: disconnection the serial
# listen_load: install the handler for the envets
# listen_unload: uninstall the handler
# set_nixie: nixie show
# write_mem: write the mem
# read_mem: read the mem
# clear_mem: clear the mem
# buzzer_start: start the buzzer
# buzzer_stop: stop the buzzer
class SerAction():
    def __init__(self):
        self.ser = BasicSerAction()

        # define the oders
        self.order_open_first_hand = 0xff
        self.order_open_second_hand = 0xf0
        self.order_open_third_hand = 0xf1

        self.order_key1 = 0xb1
        self.order_key2 = 0xb2
        self.order_key3 = 0xb3
        self.order_up = 0xa1
        self.order_down = 0xa2
        self.order_left = 0xa3
        self.order_right = 0xa4
        self.order_enter = 0xa0
        self.order_vibrate = 0xc8

        self.order_nixie_start = 0x80
        self.order_nixie_end = 0x8f

        self.order_mem_write_start = 0x20
        self.order_mem_write_end = 0x2f

        self.order_mem_read_start = 0x60
        self.order_mem_read_end = 0x6f


        # flags
        self.connected = 0

        # listen hander
        self.key1_handler = self.__empty_handler
        self.key2_handler = self.__empty_handler
        self.key3_handler = self.__empty_handler
        self.up_handler = self.__empty_handler
        self.down_handler = self.__empty_handler
        self.left_handler = self.__empty_handler
        self.right_handler = self.__empty_handler
        self.enter_handler = self.__empty_handler
        self.vibrate_handler = self.__empty_handler

        self.key1_handler_arguments = []
        self.key2_handler_arguments = []
        self.key3_handler_arguments = []
        self.up_handler_arguments = []
        self.down_handler_arguments = []
        self.left_handler_arguments = []
        self.right_handler_arguments = []
        self.enter_handler_arguments = []
        self.vibrate_handler_arguments = []

        # timer
        self.receive_timer = Timer(0.01, self.__receive_data_on_time)

        # nixie char
        self.character = {'a' : 0x77, 'b' : 0x7f, 'c' : 0x39, 'd' : 0x3f, 'e' : 0x79, 'f' : 0x71, 'g' : 0x3d, 'h' : 0x76, 'i' : 0x06,  # a, b, c, d, e, f, g, h, i
                    'j' : 0x1e, 'k' : 0xf6, 'l' : 0x38, 'm' : 0x4f, 'n' : 0x37, 'o' : 0x3f, 'p' : 0x73, 'q' : 0xbf, 'r' : 0xf7,  # j, k, l, m, n, o, p, q, r
                    's' : 0x6d, 't' : 0x07, 'u' : 0x62, 'v' : 0x3e, 'w' : 0xf9, 'x' : 0xf6, 'y' : 0xe6, 'z' : 0xdb,  # s, t, u, v, w, z, y, z
                    '0': 0x3f, '1': 0x06, '2': 0x5b, '3': 0x4f, '4': 0x66, '5': 0x6d, '6': 0x7d, '7': 0x07, '8': 0x7f, '9': 0x6f, ' ': 0x00}

        self.tone =         \
            [
                0xf8, 0x8c, # 低八度，低1
                0xf9, 0x5b,
                0xfa, 0x15, # 低3
                0xfa, 0x67,
                0xfb, 0x04, # 低5
                0xfb, 0x90,
                0xfc, 0x0c, # 低7
                0xfc, 0x44, # 中央C调
                0xfc, 0xac, # 中2
                0xfd, 0x09,
                0xfd, 0x34, # 中4
                0xfd, 0x82,
                0xfd, 0xc8, # 中6
                0xfe, 0x06,
                0xfe, 0x22, # 高八度，高1
                0xfe, 0x56,
                0xfe, 0x6e, # 高3
                0xfe, 0x9a,
                0xfe, 0xc1, # 高5
                0xfe, 0xe4,
                0xff, 0x03 # 高7
            ]

    def __empty_handler(self, arguments):
        return

    def __receive_data_on_time(self):
        try:
            instructions = self.ser.port_receive()

            if instructions:
                for instruction in instructions:
                   #print(instruction)
                    if instruction == self.order_key1:
                        self.key1_handler(self.key1_handler_arguments)
                    elif instruction == self.order_key2:
                        self.key2_handler(self.key2_handler_arguments)
                    elif instruction == self.order_key3:
                        self.key3_handler(self.key3_handler_arguments)
                    elif instruction == self.order_up:
                        self.up_handler(self.up_handler_arguments)
                    elif instruction == self.order_down:
                        self.down_handler(self.down_handler_arguments)
                    elif instruction == self.order_left:
                        self.left_handler(self.left_handler_arguments)
                    elif instruction == self.order_right:
                        self.right_handler(self.right_handler_arguments)
                    elif instruction == self.order_enter:
                        self.enter_handler(self.enter_handler_arguments)
                    elif instruction == self.order_vibrate:
                        self.vibrate_handler(self.vibrate_handler_arguments)

            if self.connected == 1:
                self.receive_timer = Timer(0.01, self.__receive_data_on_time)
                self.receive_timer.start()

        except:
            pass

    # connection:
    # Argument:
    # Return: 0 for failure, 1 for success
    def connection(self):
        for _ in range(0, 20):
            ports = self.ser.port_check()

            if ports:
                for port in ports:
                    if self.ser.port_open(port[0]):
                        # give each port three chance to try to connect
                        for _ in range(0, 3):

                            # 1st hand: give the serial the request
                            self.ser.port_send(self.order_open_first_hand)

                            # 2nd hand: receive the request from the serial
                            for _ in range(0, 10):
                                self.receive_timer.cancel()
                                time.sleep(0.01)
                                data = self.ser.port_receive()
                                if data:
                                    if data.pop(-1) == self.order_open_second_hand:
                                        # 3rd hand: give the serial success flag
                                        self.ser.port_send(self.order_open_third_hand)
                                        self.connected = 1
                                        self.__receive_data_on_time()
                                        return 1

        return 0

    # disconnection:
    # Argument:
    # Return: 0 for failure, 1 for success
    def disconnection(self):
        try:
            self.connected = 0
            self.ser.port_close()
            return 1
        except:
            return 0

    # listen_load:
    # Argument: item(what to listen), hander(function to do), argue(argument)
    # Return: 0 for failure, 1 for success
    def listen_load(self, item, hander, arguments):
        try:
            if item == 'key1':
                self.key1_handler = hander
                self.key1_handler_arguments = arguments
            elif item == 'key2':
                self.key2_handler = hander
                self.key2_handler_arguments = arguments
            elif item == 'key3':
                self.key3_handler = hander
                self.key3_handler_arguments = arguments
            elif item == 'up':
                self.up_handler = hander
                self.up_handler_arguments = arguments
            elif item == 'down':
                self.down_handler = hander
                self.down_handler_arguments = arguments
            elif item == 'left':
                self.left_handler = hander
                self.left_handler_arguments = arguments
            elif item == 'right':
                self.right_handler = hander
                self.right_handler_arguments = arguments
            elif item == 'enter':
                self.enter_handler = hander
                self.enter_handler_arguments = arguments
            elif item == 'vibrate':
                self.vibrate_handler = hander
                self.vibrate_handler_arguments = arguments
            return 1
        except:
            return 0

    # listen_load:
    # Argument: item(what to not listen)
    # Return: 0 for failure, 1 for success
    def listen_unload(self, item):
        try:
            if item == 'key1':
                self.key1_handler = self.__empty_handler
                self.key1_handler_arguments = []
            elif item == 'key2':
                self.key2_handler = self.__empty_handler
                self.key2_handler_arguments = []
            elif item == 'key3':
                self.key3_handler = self.__empty_handler
                self.key3_handler_arguments = []
            elif item == 'up':
                self.up_handler = self.__empty_handler
                self.up_handler_arguments = []
            elif item == 'down':
                self.down_handler = self.__empty_handler
                self.down_handler_arguments = []
            elif item == 'left':
                self.left_handler = self.__empty_handler
                self.left_handler_arguments = []
            elif item == 'right':
                self.right_handler = self.__empty_handler
                self.right_handler_arguments = []
            elif item == 'enter':
                self.enter_handler = self.__empty_handler
                self.enter_handler_arguments = []

            elif item == 'vibrate':
                self.vibrate_handler = self.__empty_handler
                self.vibrate_handler_arguments = []

            return 1
        except:
            return 0

    # set_nixie:
    # Argument: string(8 number stand for the number nixie shows)
    # Return: 0 for failure, 1 for success
    def set_nixie(self, strings):
        try:
            datalist = []
            for char in strings:
                datalist.append(self.character[char])


            self.ser.port_send(self.order_nixie_start)

            count = 8 - len(datalist)
            for _ in  range(0, count):
                datalist.append(0x00)
            self.ser.port_send_list(datalist)

            return self.ser.port_send(self.order_nixie_end)

        except:
            return 0

    # set_nixie_hex:
    # Argument: datalist(8 number stand for the number nixie shows)
    # Return: 0 for failure, 1 for success
    def set_nixie_hex(self, datalist):
        try:
            self.ser.port_send(self.order_nixie_start)

            count = 8 - len(datalist)
            for _ in  range(0, count):
                datalist.append(0x00)
            self.ser.port_send_list(datalist)

            return self.ser.port_send(self.order_nixie_end)


        except:
            return 0

    # set_led:
    # Argument: hex
    # Return: 0 for failure, 1 for success
    def set_led(self, hex):
        try:
            return self.ser.port_send_list([0x70, hex])
        except:
            return 0

    # write_mem:
    # Argument: addr(address), data(data to write)
    # Return: 0 for failure, 1 for success
    def write_mem(self, addr, data):
        try:
            self.ser.port_send_list([self.order_mem_write_start, addr, data, self.order_mem_write_end])
            return 1
        except:
            return 0

    # read_mem:
    # Argument: addr(address)
    # Return: data(or 0)
    def read_mem(self, addr):
        try:
            try:
                self.receive_timer.cancel()
            except:
                pass

            self.ser.port_send_list([self.order_mem_read_start, addr, self.order_mem_read_end])
            data = []
            for _ in range(0, 100000):
                data = self.ser.port_receive()
                if data:
                    break
            self.receive_timer = Timer(0.01, self.__receive_data_on_time)
            self.receive_timer.start()
            return data[-1]
        except:
            return -1

    # clear_mem:
    # Argument: item(what to not listen)
    # Return: 0 for failure, 1 for success
    def clear_mem(self):
        try:
            for i in range(0, 256):
                self.write_mem(i, 0)

            return 1
        except:
            return 0

    # buzzer_start:
    # Argument:
    # Return: 0 for failure, 1 for success
    def buzzer_start(self):
        try:
            return self.ser.port_send(0x40)
        except:
            return 0

    # buzzer_stop:
    # Argument:
    # Return: 0 for failure, 1 for success
    def buzzer_stop(self):
        try:
            return self.ser.port_send(0x4f)
        except:
            return 0

    # buzzer_tone:
    # Argument:datalist(high, low)
    # Return: 0 for failure, 1 for success
    def buzzer_tone(self, datalist):
        try:
            return self.ser.port_send_list([0x50, datalist[0], datalist[1], 0x5f])
        except:
            return 0

    def buzzer_tone_music(self, tone):
        try:
            return self.ser.port_send_list([0x50, self.tone[tone], self.tone[tone + 1], 0x5f])
        except:
            return 0


    def send_485(self, data):
        try:
            return self.ser.port_send_list([0xe0, data])
        except:
            return 0

    def get_485_buffer(self):
        try:
            try:
                self.receive_timer.cancel()
            except:
                pass

            self.ser.port_send(0xe8)
            data = []
            for _ in range(0, 100000):
                data = self.ser.port_receive()
                if data:
                    break
            self.receive_timer = Timer(0.01, self.__receive_data_on_time)
            self.receive_timer.start()
            return data
        except:
            return []




