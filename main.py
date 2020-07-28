
import config
from scheduler import Scheduler
from aiogram import Bot, Dispatcher, executor, types

COMMANDS_LIST = {
    '!start' : 'Start bot',
    '!help' : 'Show available commands',
    '!schedule' : 'Create schedule',
    '!shedule_day' : "Create a day note for your schedule"
    }

bot = Bot(token = config.API_TOKEN)
dp = Dispatcher(bot)

# --- Можно сделать все комманды в отдельном файле ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi !\nI'm Dandelion_bot !\n Run /help to see available commands !")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    response = ""
    for command, description in COMMANDS_LIST.items():
        line = command + "  -  " + description + "\n " 
        response += line
    await message.answer(f'Available commands: \n\n {response}')

# будет создавать расписание с названием и закидывать в БД к текущему юзеру
#  !!! это нужно сделать 1ым когда разберемся с SQL
# @dp.message_handler(commands=['schedule'])  # !shedule -> user_message -> message.text -> sdlr.raw_msg -> schedule_name -> name of schedule in database 

@dp.message_handler(commands=['schedule_day'])
async def create_day(message: types.Message):
    
    ScheduleWelcomeMessage = "Fill the schedule with this schema :\n\nDay of the week\nItem_1-begin_time-end_time\nItem_2...\n\nWrite time like this: 14:00. There you create schema for 1 day only!"
    await message.answer(ScheduleWelcomeMessage)
    
    @dp.message_handler(lambda message: message.text and message.text.lower() != "")
    async def create_shedule_day(message: types.Message):
        
        # create Scheduler and invoke function
        sdlr = Scheduler(message.text)                  
        sdlr.set_schedule_day()
    

@dp.message_handler(commands=['notif'])
async def manage_notifier(message: types.Message):
    
    await message.answer('Здесь пока ничего нет :)')    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = config.SKIP_UPDATE_STATUS) 
