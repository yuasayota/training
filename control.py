import tkinter as tk
import tkinter.messagebox as messagebox
import User_data as ud
import User
import sqlite3
import time
import threading
from datetime import datetime, timedelta


class Muscle_APP(User.User):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("筋肉トレーニング")
        self.window.geometry("800x500")
        self.data_manager = ud.data()
        self.create_widgets()
        self.show_all_data()

    def create_widgets(self):

        self.complete_Button = tk.Button(
            self.window, text="完了", command=self.countdown_timer)
        self.complete_Button.place(x=500, y=10)
        self.add_Button = tk.Button(
            self.window, text="登録", command=self.open_windows)
        self.add_Button.place(x=580, y=10)

        self.RESET_Button = tk.Button(
            self.window, text="リセット", command=self.data_reset)
        self.RESET_Button.place(x=0, y=10)

        self.show_Button = tk.Button(
            self.window, text="削除", command=self.data_remove)
        self.show_Button.place(x=80, y=10)

        self.table = tk.Listbox(self.window, width=50, height=15)
        self.table.place(x=50, y=100)

        self.timer_label = tk.Label(
            self.window, text="00:00:00", font=("Helvetica", 40))
        self.timer_label.place(x=560, y=300)

    def open_windows(self):
        self.ADD_WINDOW = tk.Toplevel(self.window)
        self.ADD_WINDOW.geometry("300x300+400+200")
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

    def save_data(self):
        self.TRAINING = self.IN_NAME.get()
        self.Number_REP = int(self.IN_REP.get())
        self.Number_SET = int(self.IN_SET.get())
        self.REST_TIME = int(self.IN_TIME.get())

        self.data_manager.DATA_SET()
        self.data_manager.DATA_IN(
            self.TRAINING, self.Number_REP, self.Number_SET, self.REST_TIME)
        self.ADD_WINDOW.destroy()
        self.show_all_data()

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
        training, rep, num_set, num_time = self.data_manager.get_all_data()[
            selected_index]
        self.data_manager.data_remove_select(training)
        messagebox.showinfo("削除", training + "のデータを削除しました！")
        self.show_all_data()

    def show_all_data(self):
        self.table.delete(0, tk.END)
        all_data = self.data_manager.get_all_data()
        for data in all_data:
            training, rep, num_set, num_time = data
            self.table.insert(
                tk.END, f"{training} - レップ数:{rep} - セット数:{num_set} - 休憩時間:{num_time}秒")

    def run(self):
        self.window.mainloop()

    def countdown_timer(self):
        selected_data = self.table.curselection()
        if not selected_data:
            messagebox.showwarning("警告", "トレーニングを選択してください。")
            return

        # 選択されたトレーニングの休憩時間を取得
        selected_index = selected_data[0]
        training, rep, num_set, num_time = self.data_manager.get_all_data()[
            selected_index]

        # セット数が0の場合は警告を表示して終了
        if num_set == 0:
            messagebox.showwarning("警告", "すべてのセットが終了しました。")
            return
        # タイマーをセット
        self.set_timer(num_time)
        self.data_manager.set_complete(num_set, training)
        self.show_all_data()

    def set_timer(self, seconds):

        end_time = datetime.now() + timedelta(seconds=seconds)
        while datetime.now() < end_time:
            remaining_time = end_time - datetime.now()
            self.timer_label.config(text=str(remaining_time)[:-7])
            self.window.update()
            time.sleep(1)
        self.show_all_data()
        self.timer_label.config(text="筋肉が刺激を欲しています！")


if __name__ == "__main__":
    app = Muscle_APP()
    app.run()

