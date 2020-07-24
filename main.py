
import config
import scheduler
from aiogram import Bot, Dispatcher, executor, types

COMMANDS_LIST = {
    '!start' : 'Start bot',
    '!help' : 'Show available commands' 
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
    
@dp.message_handler(commands=['schedule'])
async def create_shedule(message: types.Message):
    
    ScheduleWelcomeMessage = "Заполните расписание по следующей схеме:\n\nДень недели\nПункт1-время_начала-время_оконачания\nПункт2....\n\nВремя указываем так: 14:00. Расписание указывается на каждый день отдельно!"
    await message.answer(ScheduleWelcomeMessage)
    
    # create Scheduler and invoke function
    
    
@dp.message_handler(commands=['notif'])
async def manage_notifier(message: types.Message):
    
    await message.answer('Здесь пока ничего нет :)')    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = config.UPDATE_STATUS) 
