import tkinter as tk
import datetime
import requests
import pya3rt
import time
import webbrowser
import subprocess
from bs4 import BeautifulSoup
import pygame
from mutagen.mp3 import MP3 as mp3
import speech_recognition as sr
import pyperclip



#APIの取得
apikey = "YOUR API KEY"
client = pya3rt.TalkClient(apikey)

#天気情報を取得
weatherUrl = 'http://weather.livedoor.com/forecast/webservice/json/v1'
payload = {'city':'YOUR CITY NUMBERS'}
data = requests.get(weatherUrl,params=payload).json()

#音声認識に必要なオブジェクトを生成
r = sr.Recognizer()
mic = sr.Microphone()

#ウィンドウ生成
root = tk.Tk()

#ウィンドウのタイトルを定義
root.title(u'chatbot')
#ウィンドウサイズを定義
root.geometry('500x300+1400+700')

#日付を取得する
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d %H:%M")

#音源ファイルの処理
filename = 'se.mp3' #再生したいmp3ファイル
pygame.mixer.init()
pygame.mixer.music.load(filename) #音源を読み込み
mp3_length = mp3(filename).info.length #音源の長さ取得

def btn_click():
    # 録音　r.adjust_for_ambient_noise(source)はノイズ対策

    pygame.mixer.music.play(1)  # 再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(1.1)
    pygame.mixer.music.stop()  # 音源の長さ待ったら再生停止

    with mic as source:
         r.adjust_for_ambient_noise(source)
         audio = r.listen(source)
    try:
         Entry1.insert(tk.END, r.recognize_google(audio, language='ja-JP'))
         addList(Entry1.get())
    except:
         pass

def addList(text):
    mysay = 'you: ' + text
    print(mysay)
    ListBox1.insert(tk.END, mysay)
    print('chatbot: '+talk(text))
    chatbot = 'chatbot: ' + talk(text)
    Entry1.delete(0,tk.END)
    addRep(chatbot)

def addRep(chatbot):
    ListBox1.insert(tk.END,chatbot)


#botの返答
def talk(say):

    if say == '今日の天気は':
        rep = 'nnn、'+ data['title']+'は'+data['forecasts'][0]['telop']+'となっています。' \
            '明日の天気は'+ data['forecasts'][1]['telop']+'の模様です。'
        pyperclip.copy(rep)
        return(rep)

    elif say == '明日の天気は':
        rep = 'nnn、明日の天気は'+ data['forecasts'][1]['telop']+'の模様です。'
        pyperclip.copy(rep)
        return(rep)

    elif say == 'Ok Google':
        rep = 'nn、私はそんなに優秀ではありません。' \
              'Google先生に失礼です。'
        pyperclip.copy(rep)
        return(rep)

    elif say == 'Hey Siri':
        rep = 'nn、 お使いのデバイスはパソコンです。勘違いしないでよね！'
        pyperclip.copy(rep)
        return(rep)

    elif say == 'コルタナさん':
        rep = 'nn、コルタナさん、かわいいよね。'
        pyperclip.copy(rep)
        return(rep)

    elif say =='YouTube を開いて':
        webbrowser.open('https://www.youtube.com/?hl=ja&gl=JP')
        Entry1.delete(0,tk.END)

    elif say =='Google を開いて':
        webbrowser.open('https://www.google.com')
        Entry1.delete(0,tk.END)

    elif say == '朝起こして':
        rep = 'nn、目覚ましを起動しました'
        subprocess.Popen(r'explorer.exe shell:AppsFolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App')
        pyperclip.copy(rep)
        return(rep)

    elif say == '今日のニュース':
        Entry1.delete(0, tk.END)
        html = requests.get('https://news.yahoo.co.jp/pickup/rss.xml')
        yahoo = BeautifulSoup(html.content, "html.parser")

        for title in yahoo.select("title"):
             print(title.getText())
             ListBox1.insert(tk.END,title.getText())

    elif say == '終了':
        rep = 'nn、動作を終了します'
        pyperclip.copy(rep)
        time.sleep(2)
        root.quit()
        return(rep)

    elif say == 'じゃあね':
        rep = 'nnn、またお会いしましょう'
        pyperclip.copy(rep)
        time.sleep(2)
        p.kill()
        root.quit()
        return(rep)

    else:
        ans_json = client.talk(say)
        ans = 'nn、'+ ans_json['results'][0]['reply']
        pyperclip.copy(ans)
        return(ans)


Sratic = tk.Label(text=u'トーク')
Sratic.pack(anchor="nw")

#リストボックスを設置する
ListBox1 = tk.Listbox(width=70,height=13)
ListBox1.pack()

Sratic1 = tk.Label(text=u'下に入力して検索')
Sratic1.pack(anchor="nw")

#Entryを出現させる
Entry1 = tk.Entry(font=("",17),width=30)
Entry1.pack(anchor="nw",side="left")

#"Talk'ボタンを生成
Button = tk.Button(text=u'Talk',width=5,height=2,command=btn_click)
Button.pack(anchor="ne",side="right")

#"Send'ボタンを生成
Button1 = tk.Button(text=u'Send',width=5,height=2,command=lambda:addList(Entry1.get()))
Button1.pack(anchor="ne",side="right")


root.mainloop()
