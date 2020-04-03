# Cuser
A new way to develop STC.

[![asciicast](video.png)](https://youtu.be/iLaqNKXIfCY)

## 安装

获取上位机：

```shell
pip install cuser
```

获取下位机：

```
git clone https://github.com/CynricFeng/Cuser.git
```

## 使用

```python
from cuser import SerAction

ser = SerAction()
# 上位机和下位机自动连接配对
ser.connection()
```

## 功能

### BasicSerAction

|       操作        |        描述        |             参数             |           返回           |
| :---------------: | :----------------: | :--------------------------: | :----------------------: |
|   port_check()    |      端口监测      |                              |       可用端口列表       |
| port_open(*port*) |      端口打开      |     需要打开的端口的名称     |   成功返回1，失败返回0   |
|   port_close()    | 关闭正在使用的端口 |                              |   成功返回1，失败返回0   |
| port_send(*data*) |  发送单个八位数据  |       一个八位的二进制       |   成功返回1，失败返回0   |
| port_send_list()  |    发送多个数据    | 一个含有多个八位二进制的列表 |   成功返回1，失败返回0   |
|  port_receive()   |    接收多个数据    |                              | 返回接收列表（可以为空） |

### SerAction

|                    操作                    |               描述               |                      参数                      |              返回              |
| :----------------------------------------: | :------------------------------: | :--------------------------------------------: | :----------------------------: |
|                connection()                |         自动与下位机配对         |                                                |      成功返回1，失败返回0      |
|              disconnection()               |         与下位机断开配对         |                                                |      成功返回1，失败返回0      |
| listen_load(*item*, *hander*, *arguments*) |         对下位机原件监听         | 监听事项，触发时调用的函数，函数所需的参数列表 |      成功返回1，失败返回0      |
|           listen_unload(*item*)            |         对下位机取消监听         |                 取消监听的事项                 |                                |
|            set_nixie(*strings*)            |            设置数码管            |        需要显示的字母或者整数（字符串）        |      成功返回1，失败返回0      |
|         set_nixie_hex(*datalist*)          |        用七段码设置数码管        |           需要显示的数据的二进制列表           |      成功返回1，失败返回0      |
|               set_led(*hex*)               |             设置LED              |                  一个二进制数                  |      成功返回1，失败返回0      |
|         write_mem(*addr*, *data*)          | 向非易失存储器中储存一个八位数据 |             储存的地址，储存的数据             |      成功返回1，失败返回0      |
|              read_mem(*addr*)              | 向非易失存储器中读取一个八位数据 |                   读取的地址                   |    成功返回数据，失败返回-1    |
|                clear_mem()                 |   清空非易失存储器中的所有数据   |                                                |      成功返回1，失败返回0      |
|               buzzer_start()               |            打开蜂鸣器            |                                                |      成功返回1，失败返回0      |
|               buzzer_stop()                |            关闭蜂鸣器            |                                                |      成功返回1，失败返回0      |
|          buzzer_tone(*datalist*)           |         设置蜂鸣器的音调         |      定时器频率的高八位和第八位组成的列表      |      成功返回1，失败返回0      |
|         buzzer_tone_music(*tone*)          |          设置蜂鸣器音调          |                    音调的值                    |      成功返回1，失败返回0      |
|              send_485(*data*)              |       通过485端口发送数据        |                  数据的二进制                  |      成功返回1，失败返回0      |
|              get_485_buffer()              |      接收485端口收到的数据       |                                                | 返回接收的数据的列表（可为空） |
|              vibrate_start()               |        打开震动传感器监听        |                                                |      成功返回1，失败返回0      |
|               vibrate_end()                |        关闭震动传感器监听        |                                                |      成功返回1，失败返回0      |



