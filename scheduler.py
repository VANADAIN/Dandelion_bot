
import sqlite3

class Database():
    def __init__(self):
        pass
    
    # use as decorator
    # opens db connection -> returns result of a callable function -> closes connection
    def ensure_connection(function):
        
        def inner(*args, **kwargs):
            
            with sqlite3.connect('users.db') as connection:
                res = function(conn = connection, c = connection.cursor(), *args, **kwargs)
            return res
        
        return inner
    
    @ensure_connection
    def init_table(self, conn, c):

        c.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id     text,
                sched_name  text,
                day         text,
                B_time_H    int,
                B_time_M    int,
                E_time_H    int,
                E_time_M    int
            )""")
        conn.commit()
        
# отвечает за создание, перезапись, удаление расписания в БД
class Scheduler():
    
    def __init__(self, msg_txt):
        
        self.raw_msg = msg_txt 
    
    def get_user_id(self, id):
        
        sefl.user_id = id
        
    def set_schedule(self):
        name = self.raw_msg
    
    def set_schedule_day(self):
    # парсим и записываем параметры расписания
        parsed_str = self.raw_msg.split('\n')
        
        day_dict = {"day" : {
            
                     "name" : parsed_str[0].strip(), # tuesday
                     "day_items" : {
                           
                           # "item_1" : {
                                # "begin_time" :
                                # "end_time": 
                                #}
                                
                            }
                        }
                    }
        
        for i in range(1, len(parsed_str)):
            # разбиваем айтем на слова через дефис как указано в отправленном сообщении
            # 0 - название, 1 - время начала, 2 - время конца
            # используем трим чтобы убрать лишние пробелы
            words = parsed_str[i].split("-")
            
            # обновляем записи в словаре
            day_dict["day"]["day_items"].update({
                words[0].strip() : {
                    "begin_time": words[1].strip(),
                    "end_time": words[2].strip()
                    }
                })
        
        # записываем day_dict в выбранный schedule к текущему юзеру
            
        
            
    
    # --- пока не уверен нужно ли это ---
    #def check_schedule_day():
    #выполняем перед записью (введено ли все правильно)
        #pass
    
    def write_schedule_day():
    # запись в БД
        pass
    
    def rewrite_schedule_day():
    # перезаписать день -> вызывается после check_schedule и меняет raw_msg
    # если что-то указано неправильно или в случае когда поменялись пункты/время 
        pass
    
    def delete_shedule_day():
        pass
    
    def delete_schedule():
    # удалить все дни 
        pass
    
