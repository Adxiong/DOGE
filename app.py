import threading

import asyncio
import tkinter as tk
import  datetime
import json
from aiowebsocket.converses import AioWebSocket
import requests
import time as t


root = tk.Tk()
status = False
res = tk.StringVar(root)
LMon = tk.Label(root)
Llv = tk.Label(root)
Ltime = tk.Label(root)
InitMon = tk.Entry(root)
huilv = 0

async def Start(url,num):
    global status
    global LMon
    global Ltime
    global Llv
    async with AioWebSocket(url) as aws:
        converse = aws.manipulator
        n = 0
        message = '{"event": 17, "SpotCandleMap": {"marketId": 108, "period": "15m", "symbol": "DOGE", "anchor": "USDT","language": "zh_cn", "time": null, "legal_currency": "CNY","platform": "web_pc"}, "requestId": '+ str(int(t.time())) + '}'
        await converse.send(message)
        while status:
            mes = await converse.receive()
            n += 1
            if n % 5 == 0:
                n = 0
                await converse.send(message)

            if(mes):
                avg = json.loads(str(mes , 'utf-8'))
                # print(avg['kline'][0]['close'])
                Llv.configure(text=avg['kline'][0]['close'])
                Llv.update()
                Ltime.configure(text=datetime.datetime.now())
                Ltime.update()
                LMon.configure(text="持有 "+str(round(float(num)*huilv*avg['kline'][0]['close'],4))+" 元")
                LMon.update()
                # print(datetime.datetime.now())
            else:
                # print("歇逼")
                pass



def startEvent():
    global status
    status = True
    asyncio.run(Start(URL,InitMon.get()))

def stopEvent():
    global status
    status = False

def getHuilV():
    global huilv
    url = 'https://webapi.huilv.cc/api/exchange?num=1&chiyouhuobi=USD&duihuanhuobi=CNY'
    res = requests.get(url=url).json()
    huilv = float(res['dangqianhuilv'])


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    t.setName('tool')
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！



if __name__ == "__main__":
    getHuilV()
    time = datetime.datetime.now()
    URL ="wss://ws2.mytokenapi.com/"

    root.geometry('320x160')
    root.title("熊菲特的成功之路")
    root.wm_attributes('-topmost', 1)
    InitMon.insert(0, "0")
    InitMon.pack()
    Btn = tk.Button(root,text="开始监控",command=lambda :thread_it(startEvent))
    Btn.pack()
    Btn = tk.Button(root, text="停止监控", command=lambda :thread_it(stopEvent))
    Btn.pack()
    Ltime.configure(text=datetime.datetime.now())
    Ltime.pack()
    Llv.configure(text="汇率")
    Llv.pack()
    LMon.configure(text="金额")
    LMon.pack()
    root.mainloop()
