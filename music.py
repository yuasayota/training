
import importlib
import tkinter as tk
import pygame.mixer as pyx


class Sound():
    a = 0

    def sound():
        pyx.init()  # 初期化
        playlist = ["music/チャーリープース.mp3", "music/attention.mp3"]
        for p in playlist:
            pyx.init()
            pyx.music.load(p)
            mc = mp3(p).info.length  # 音源の長さを取得
            pyx.music.play(1, 600)  # 再生

            root = tk.Tk()
            cvs = tk.Canvas(width=100, height=100)
            cvs.pack()
            tk.Button(text="一時停止", command=Sound.stop, height=1, pady=2).pack(
                side=tk.TOP, expand=True, anchor=tk.S)
            root.mainloop()

    def stop():
        if Sound.a % 2 == 1:
            pyx.music.unpause()
            Sound.a += 1

        else:
            pyx.music.pause()
            Sound.a += 1


if __name__ == '__main__':
    Sound.sound()
