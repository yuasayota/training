import tkinter as tk
import tkinter.messagebox as messagebox
import User_data as ud
import User
import sqlite3
import time
import threading
from datetime import datetime, timedelta
import pygame.mixer as pyx


class Muscle_APP(User.User):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("筋肉トレーニング")
        self.window.geometry("800x500")
        self.data_manager = ud.data()
        self.create_widgets()
        self.show_all_data()
        self.open_windows()

    def create_widgets(self):
        self.START_Button = tk.Button(
            self.window, text="開始", command=self.countdown_timer)
        self.START_Button.place(x=0, y=10)

        # self.label = tk.Label(text='テキスト')
        # self.label.pack()
        self.RESET_Button = tk.Button(
            self.window, text="データ削除", command=self.data_reset)
        self.RESET_Button.place(x=0, y=10)

        self.time_label = tk.Label(
            self.window, text="今日のトレーニング時間00:00:00", font=("Helvetica", 40))
        self.time_label.place(x=100, y=20)

        self.edit_Button = tk.Button(
            self.window, text="トレーニング時間登録", command=self.open_time_windows)
        self.edit_Button.place(x=500, y=95)

        self.add_Button = tk.Button(
            self.window, text="メニュー登録", command=self.open_windows)
        self.add_Button.place(x=500, y=125)

        self.delate_Button = tk.Button(
            self.window, text="削除", command=self.data_remove)
        self.delate_Button.place(x=500, y=155)

        self.delate_Button = tk.Button(
            self.window, text="完了度リセット", command=self.set_zero)
        self.delate_Button.place(x=560, y=155)

        self.complete_Button = tk.Button(
            self.window, text="スタート", command=self.training_timer, height=2, width=30)
        self.complete_Button.place(x=500, y=180)

        self.st = tk.Button(
            self.window, text="音楽一時停止/再開", command=self.stop, height=2, width=30)
        self.st.place(x=500, y=215)

        self.complete_Button = tk.Button(
            self.window, text="完了", command=self.countdown_timer, height=5, width=30)
        self.complete_Button.place(x=500, y=255)

        self.table = tk.Listbox(self.window, width=50, height=15)
        self.table.place(x=50, y=100)

        self.timer_label = tk.Label(
            self.window, text="休憩時間00:00:00", font=("Helvetica", 40))
        self.timer_label.place(x=200, y=400)

    def open_time_windows(self):
        self.ADD_TIME_WINDOW = tk.Toplevel(self.window)
        self.ADD_TIME_WINDOW.geometry("220x260+570+50")
        self.ADD_TIME_WINDOW.title("トレーニング時間（分）")

        tk.Label(self.ADD_TIME_WINDOW, font=30).pack()
        self.IN_TR_TIME = tk.Entry(self.ADD_TIME_WINDOW)
        self.IN_TR_TIME.pack()

        tk.Button(self.ADD_TIME_WINDOW, text="決定",
                  command=self.save_time_data).pack()

    def open_windows(self):
        self.ADD_WINDOW = tk.Toplevel(self.window)
        self.ADD_WINDOW.geometry("220x260+810+50")
        self.ADD_WINDOW.title("登録")

        tk.Label(self.ADD_WINDOW, text="トレーニング名", font=30).pack()
        self.IN_NAME = tk.Entry(self.ADD_WINDOW)
        self.IN_NAME.pack()

        tk.Label(self.ADD_WINDOW, text="レップ数", font=30).pack()
        self.IN_REP = tk.Entry(self.ADD_WINDOW)
        self.IN_REP.pack()

        tk.Label(self.ADD_WINDOW, text="セット数", font=30).pack()
        self.IN_SET = tk.Entry(self.ADD_WINDOW)
        self.IN_SET.pack()

        tk.Label(self.ADD_WINDOW, text="休憩時間(秒)", font=30).pack()
        self.IN_TIME = tk.Entry(self.ADD_WINDOW)
        self.IN_TIME.pack()

        tk.Button(self.ADD_WINDOW, text="登録", command=self.save_data).pack()

    def save_time_data(self):
        self.TR_TIME = int(self.IN_TR_TIME.get())
        print(self.TR_TIME)
        self.data_manager.DATA_SET2()
        self.data_manager.DATA_IN2(
            self.TR_TIME)
        print(self.data_manager.get_all_data2())
        self.ADD_TIME_WINDOW.destroy()
        self.show_all_data()

    def save_data(self):
        self.TRAINING = self.IN_NAME.get()
        self.Number_REP = int(self.IN_REP.get())
        self.Number_SET = int(self.IN_SET.get())
        self.REST_TIME = int(self.IN_TIME.get())

        self.data_manager.DATA_SET()
        self.data_manager.DATA_IN(
            self.TRAINING, self.Number_REP, 0, self.Number_SET, 0, self.REST_TIME)
        self.ADD_WINDOW.destroy()
        self.show_all_data()

    def training_timer(self):
        try:
            seconds = self.data_manager.get_all_data2()[0]*60
        except TypeError:
            messagebox.showwarning("警告", "トレーニング時間登録を設定してください。")
            return
        self.sound()
        seconds = self.data_manager.get_all_data2()[0]*60
        end_time = datetime.now() + timedelta(seconds=seconds)
        while datetime.now() < end_time:
            remaining_time = end_time - datetime.now()
            self.time_label.config(text=str(remaining_time)[:-7])
            self.window.update()
            time.sleep(1)
        self.data_manager.DATA_REMOVE_TIME()
        self.show_all_data()
        pyx.init()
        clear = pyx.Sound("music/クリア.mp3")
        clear.play(0)
        time.sleep(3)
        pyx.fadeout()
        self.time_label.config(text="you win")

    def data_reset(self):
        self.data_manager.DATA_REMOVE_ALL()
        messagebox.showinfo("削除", "全データを削除しました！")
        self.show_all_data()

    def data_remove(self):
        selected_data = self.table.curselection()
        if not selected_data:
            messagebox.showwarning("警告", "トレーニングを選択してください。")
            return
        selected_index = selected_data[0]
        training, rep, clear, num_set, parsent, num_time = self.data_manager.get_all_data()[
            selected_index]
        self.data_manager.data_remove_select(training)
        messagebox.showinfo("削除", training + "のデータを削除しました！")
        self.show_all_data()

    def set_zero(self):
        self.data_manager.set_reset()
        self.show_all_data()

    def show_all_data(self):
        self.table.delete(0, tk.END)
        all_data = self.data_manager.get_all_data()
        for data in all_data:
            training, rep, clear, num_set, parsent, num_time = data
            self.table.insert(
                tk.END, f"{training} - レップ数:{rep} - 完了度:{clear}/{num_set} {parsent}%- 休憩時間:{num_time}秒")

    def countdown_timer(self):
        selected_data = self.table.curselection()
        if not selected_data:
            messagebox.showwarning("警告", "トレーニングを選択してください。")
            return

        # 選択されたトレーニングの休憩時間を取得
        selected_index = selected_data[0]
        training, rep, clear, num_set, parsent, num_time = self.data_manager.get_all_data()[
            selected_index]
        # タイマーをセット
        self.set_timer(num_time)
        if num_set == clear+1:
            pyx.init()
            clear = pyx.Sound("music/クリア.mp3")
            clear.play(0)
            self.timer_label.config(text=training + '完了　素晴らしい！！')
        else:
            self.timer_label.config(text="筋肉が刺激を欲しています！")
        self.data_manager.set_complete(clear, num_set, training)
        # self.all_complete()
        self.show_all_data()

    def set_timer(self, seconds):
        end_time = datetime.now() + timedelta(seconds=seconds)
        while datetime.now() < end_time:
            remaining_time = end_time - datetime.now()
            seconds -= 1
            self.timer_label.config(text=str(remaining_time)[:-7])
            self.window.update()
            if seconds == 3:
                pyx.init()
                ararm = pyx.Sound("music/カウントダウン電子音.mp3")
                ararm.play(0)
            time.sleep(1)
        self.show_all_data()

    def sound(self):
        self.a = 0
        pyx.init()
        pyx.music.load("music/test.mp3")
        pyx.music.play(-1)  # 再生

    def stop(self):
        try:
            if self.a % 2 == 1:
                pyx.music.unpause()
                self.a += 1

            else:
                pyx.music.pause()
                self.a += 1
        except AttributeError:
            messagebox.showwarning("警告", "スタートを押すと音楽が流れます")
            return

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Muscle_APP()
    app.run()
