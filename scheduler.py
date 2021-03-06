
from database import Database
# отвечает за создание, перезапись, удаление расписания в БД


class Scheduler():

    def __init__(self, msg_txt):

        self.raw_msg = msg_txt

    def set_schedule_name(self):
        sch_name = self.raw_msg
        return sch_name

    def get_user_id(self, id):
        return id

    def set_schedule_day(self):
        # парсим и записываем параметры расписания
        parsed_str = self.raw_msg.split('\n')

        day_dict = {"day": {
            "sched_name": parsed_str[0].strip(),
            "name": parsed_str[1].strip().lower(),  # tuesday
            "day_items": {

            }
        }
        }

        for i in range(2, len(parsed_str)):
            # разбиваем айтем на слова через дефис как указано в отправленном сообщении
            # 0 - название, 1 - время начала, 2 - время конца
            # используем трим чтобы убрать лишние пробелы
            words = parsed_str[i].split("-")

            # обновляем записи в словаре
            bt = words[1].strip().split(":")
            et = words[2].strip().split(":")

            bth = int(bt[0])
            btm = int(bt[1])
            eth = int(et[0])
            etm = int(et[1])

            day_dict["day"]["day_items"].update({
                words[0].strip(): {
                    "begin_time_H": bth,
                    "begin_time_M": btm,
                    "end_time_H": eth,
                    "end_time_M": etm,
                }
            })
        return day_dict

    async def write_schedule_day(self, day_info, id):

        for i in day_info['day']['day_items']:
            val = [k for k in day_info['day']['day_items'][i].values()]

            checkpoint_min = int(val[1]) - 10
            checkpoint_h = int(val[0])
            if checkpoint_min < 0:
                checkpoint_min = 60 + checkpoint_min
                if checkpoint_h != 0:
                    checkpoint_h = checkpoint_h - 1
                else:
                    checkpoint_h = 23
            arr = [id, day_info['day']['sched_name'], day_info['day']['name'], i, val[0],
                   val[1], checkpoint_h, checkpoint_min, val[2], val[3]]

            db = Database()
            await db.write_info(insert=arr)

    def rewrite_schedule_day(self):
        pass

    def delete_shedule_day(self):
        pass

    def delete_schedule(self):
        pass
