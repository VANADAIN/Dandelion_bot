
# отвечает за рассылку уведомления
from database import Database
import datetime
import calendar


class Notifier():

    def __init__(self):
        self.ENABLED = True

    def switch_activity(self):
        if self.ENABLED == False:
            self.ENABLED = True
            return "Notifier enabled"
        else:
            self.ENABLED = False
            return "Notifier disabled"

    def get_now(self):
        # *current info
        day = datetime.datetime.today().strftime('%A').lower()
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        return day, hour, minute

    def get_schedule_info(self):
        day, hour, minute = self.get_now()
        db = Database()
        print("looking in database")
        data = db.create_response(day, hour, minute)
        print(f"DATA: {data}")  # [(), ()]
        return data

    def get_week_num(self, day=datetime.datetime.now().day,
                     month=datetime.datetime.now().month, year=datetime.datetime.now().year):
        calendar_ = calendar.TextCalendar(calendar.MONDAY)
        lines = calendar_.formatmonth(year, month).split('\n')
        days_by_week = [week.lstrip().split() for week in lines[2:]]
        str_day = str(day)
        for index, week in enumerate(days_by_week):
            if str_day in week:
                return index + 1

    def prepare_notification(self):
        print("Getting info from schedule!")
        data = self.get_schedule_info()
        if data == []:
            print("false in prepare notification")
            return False
        else:
            print(f'DATA - - {data}')
            for line in data:
                user = line[0]
                name = line[1]
                note = line[2]
                B_time_H = line[3]
                B_time_M = line[4]
                E_time_H = line[5]
                E_time_M = line[6]
                number = self.get_week_num()
                msg = (
                    user, f"Num:{number}\n{name}\n{note}\n{B_time_H}:{B_time_M}-{E_time_H}:{E_time_M}")

                # check this because int destroys 0 in minute
                if B_time_M < 10 and E_time_M < 10:
                    B_time_M = [0, B_time_M]
                    E_time_M = [0, E_time_M]
                    msg = (
                        user, f"Num: {number}\n{name}\n{note}\n{B_time_H}:{B_time_M[0]}{B_time_M[1]}-{E_time_H}:{E_time_M[0]}{E_time_M[1]}")

                elif B_time_M < 10:
                    B_time_M = [0, B_time_M]
                    msg = (
                        user, f"Num: {number}\n{name}\n{note}\n{B_time_H}:{B_time_M[0]}{B_time_M[1]}-{E_time_H}:{E_time_M}")

                elif E_time_M < 10:
                    E_time_M = [0, E_time_M]
                    msg = (
                        user, f"Num: {number}\n{name}\n{note}\n{B_time_H}:{B_time_M}-{E_time_H}:{E_time_M[0]}{E_time_M[1]}")

            return msg

    def send_notification(self):
        print("-- Looking in prepare notification --")
        resp = self.prepare_notification()
        if resp == False:
            return False
        else:
            user_id = resp[0]
            text = resp[1]
            print('Sending TO BOT !!! Wooo hooooooo')
            return user_id, text
