# coding=utf-8
# 0->60 秒
# 0->60 分
# 0->60 时
import thread
from time import sleep


def clock():
    seconds = 0  # 秒针
    minute = 0  # 分针
    hour = 0  # 时针
    while True:  # 一直循环下去
        # 等待一秒钟
        if seconds < 60:
            seconds += 1
        elif seconds == 60:
            seconds = 0
            minute += 1
            if minute < 60:
                minute += 1
            elif minute == 60:
                hour += 1
                if hour < 24:
                    hour += 1
                elif hour == 24:
                    hour = 0
                    # 打印当前时间
        print("%s:%s:%s" % (hour, minute, seconds))
        sleep(1)  # 每秒钟执行一次


clock()
