import sqlite3


class Database():
    def __init__(self):
        pass

    def init_table(self):
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id         text,
                    sched_name      text,
                    day             text,
                    note            text,
                    B_time_H        int,
                    B_time_M        int,
                    checkpoint_H    int,
                    checkpoint_M    int,  
                    E_time_H        int,
                    E_time_M        int
                )""")
            conn.commit()

    def write_info(self, insert):
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (user_id, sched_name, day, note, B_time_H, B_time_M, checkpoint_H, checkpoint_M, E_time_H, E_time_M) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (insert[0], insert[1], insert[2], insert[3], insert[4], insert[5], insert[6], insert[7], insert[8], insert[9]))
            conn.commit()

    def create_response(self, day, hour, minute):
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            # use current datetime to return all values with checkpoint to notificator
            c.execute(
                "SELECT * FROM users WHERE day=? AND checkpoint_H AND Checkpoint_M=?", (day, hour, minute))
            data = c.fetchall()
        return data


db = Database()
db.init_table()
