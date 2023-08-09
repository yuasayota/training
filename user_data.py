import User
import sqlite3
import math


class data():
    def __init__(self, dbname='User.db', dbname2='time.db'):
        self.dbname = dbname
        self.dbname2 = dbname2
        self.con = sqlite3.connect(self.dbname)
        self.con2 = sqlite3.connect(self.dbname2)
        self.cur = self.con.cursor()
        self.cur2 = self.con2.cursor()
        self.DATA_SET
        self.DATA_SET2

    def DATA_SET(self):
        try:
            self.cur.execute(
                'CREATE TABLE Userdata (training STRING, rep INTEGER,clear INTEGER, number_set INTEGER, parsent INTEGER, rest_time INTEGER)')
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def DATA_SET2(self):
        try:
            self.cur2.execute(
                'CREATE TABLE Trainingtime (trainingtime INTEGER)')
            self.con2.commit()
        except sqlite3.OperationalError:
            pass

    def DATA_IN(self, training, rep, clear, number_set, parsent, rest_time):
        try:
            self.cur.execute('INSERT INTO Userdata VALUES(?, ?, ?, ?, ?, ?)',
                             (training, rep, clear, number_set, parsent, rest_time))
            self.con.commit()

        except sqlite3.OperationalError:
            pass

    def DATA_IN2(self, time):
        try:
            self.cur2.execute('INSERT INTO Trainingtime VALUES(?)',
                              (time,))
            self.con2.commit()

        except sqlite3.OperationalError:
            pass

    def get_all_data(self):
        try:
            self.cur.execute('SELECT * FROM Userdata')
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []

    def get_all_data2(self):
        try:
            self.cur2.execute('SELECT * FROM Trainingtime')
            return self.cur2.fetchone()
        except sqlite3.OperationalError:
            return []

    def DATA_REMOVE_ALL(self):
        try:
            self.cur.execute('DELETE FROM Userdata')
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def DATA_REMOVE_TIME(self):
        try:
            self.cur.execute('DELETE FROM Trainingtime')
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def data_remove_select(self, name):
        try:
            self.cur.execute(
                'DELETE FROM Userdata WHERE training = ?', (name,))
            self.con.commit()

        except sqlite3.OperationalError:
            pass

    def set_reset(self):
        self.cur.execute(
            "UPDATE  Userdata SET clear = 0")
        self.con.commit()

    def set_complete(self, count, set, name):
        count += 1
        parsent = count/set
        ps = math.floor(parsent*100)
        self.cur.execute(
            "UPDATE  Userdata SET clear = ?  ,parsent = ? WHERE training = ?", (count, ps, name))
        self.con.commit()

    def __del__(self):
        self.cur.close()
        self.con.close()
