from cuser import SerAction

class Mem():
    def __init__(self):
        self.data = 0
        self.temp_data = 0
        self.address = 0


def op(s):
    if s[0] == 1:
        s[1].address = (s[1].address + 1) % 256
        s[1].data = s[2].read_mem(s[1].address)
        s[1].temp_data = s[1].data
    elif s[0] == 2:
        s[1].temp_data = (s[1].temp_data + 1) % 256
    elif s[0] == 3:
        s[1].data = s[1].temp_data
        s[2].write_mem(s[1].address, s[1].data)

    s[2].set_nixie(str(s[1].address).zfill(2) + ' ' + str(s[1].data).zfill(2) + ' ' + str(s[1].temp_data).zfill(2))


s = SerAction()
m = Mem()

s.connection()

m.data = s.read_mem(m.address)
m.temp_data = s.read_mem(m.address)
s.set_nixie(str(m.address).zfill(2) + ' ' + str(m.data).zfill(2) + ' ' + str(m.temp_data).zfill(2))

s.listen_load('key1', op, [1, m, s])
s.listen_load('key2', op, [2, m, s])
s.listen_load('key3', op, [3, m, s])
