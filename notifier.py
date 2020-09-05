
# отвечает за рассылку уведомления
from database import Database
import datetime


class Notifier():

    def __init__(self):
        self.ENABLED = False

    def switch_activity(self):
        if self.ENABLED == False:
            self.ENABLED = True
            return 1, "Notifier enabled"
        else:
            self.ENABLED = False
            return 0, "Notifier disabled"

    def get_now(self):
        # *current info
        day = datetime.datetime.today().strftime('%A').lower()
        hour = datetime.datetime.now().hour()
        minute = datetime.datetime.now().minute()
        return day, hour, minute

    def get_schedule_info(self):
        day, hour, minute = self.get_now()
        db = Database()
        data = db.create_response(day, hour, minute)

        pass

    def send_notification(self):
        pass
