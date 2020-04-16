# Cuser

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

更多的样例程序可以参考 [samples](./samples)。

## 功能

### BasicSerAction

|       操作        |        描述        |             参数             |
| :---------------: | :----------------: | :--------------------------: |
|   port_check()    |      端口监测      |                              |
| port_open(*port*) |      端口打开      |     需要打开的端口的名称     |
|   port_close()    | 关闭正在使用的端口 |                              |
| port_send(*data*) |  发送单个八位数据  |       一个八位的二进制       |
| port_send_list()  |    发送多个数据    | 一个含有多个八位二进制的列表 |
|  port_receive()   |    接收多个数据    |                              |

### SerAction

|                    操作                    |               描述               |                      参数                      |
| :----------------------------------------: | :------------------------------: | :--------------------------------------------: |
|                connection()                |         自动与下位机配对         |                                                |
|              disconnection()               |         与下位机断开配对         |                                                |
| listen_load(*item*, *hander*, *arguments*) |         对下位机原件监听         | 监听事项，触发时调用的函数，函数所需的参数列表 |
|           listen_unload(*item*)            |         对下位机取消监听         |                 取消监听的事项                 |
|            set_nixie(*strings*)            |            设置数码管            |        需要显示的字母或者整数（字符串）        |
|         set_nixie_hex(*datalist*)          |        用七段码设置数码管        |           需要显示的数据的二进制列表           |
|               set_led(*hex*)               |             设置LED              |                  一个二进制数                  |
|         write_mem(*addr*, *data*)          | 向非易失存储器中储存一个八位数据 |             储存的地址，储存的数据             |
|              read_mem(*addr*)              | 向非易失存储器中读取一个八位数据 |                   读取的地址                   |
|                clear_mem()                 |   清空非易失存储器中的所有数据   |                                                |
|               buzzer_start()               |            打开蜂鸣器            |                                                |
|               buzzer_stop()                |            关闭蜂鸣器            |                                                |
|          buzzer_tone(*datalist*)           |         设置蜂鸣器的音调         |      定时器频率的高八位和第八位组成的列表      |
|         buzzer_tone_music(*tone*)          |          设置蜂鸣器音调          |                    音调的值                    |
|              send_485(*data*)              |       通过485端口发送数据        |                  数据的二进制                  |
|              get_485_buffer()              |      接收485端口收到的数据       |                                                |
|              vibrate_start()               |        打开震动传感器监听        |                                                |
|               vibrate_end()                |        关闭震动传感器监听        |                                                |

## TODO

- [ ] 对下位机进行更近一步的封装，使得下位机更加灵活，迁移性更强
- [ ] 增加上位机与下位机之间数据传输的鲁棒性

## 感谢

这个项目是在我大二小学期的时候在两周之内做出来的，当时看到周围同学不太喜欢 STC 硬件开发，所以产生了这个灵感。时间仓促，还有很多地方做的不够好。但是 Cuser 对于我们学校的开发板上的很多功能是可以稳定使用了。特别感谢那段期间罗老师、方老师的指导，也感谢邓同学和石同学对于此项目的建议。

这个项目也是在我初学硬件开发之后开发的，回头来看，也有很多很幼稚的想法。如果有学弟学妹能够使用上这个项目，有任何问题，可以与我取得联系。如果学弟学妹能够有兴趣对这个项目进行维护、重构，也很欢迎大家提交代码，或者 [与我取得联系](fengyangyang@hnu.edu.cn)。