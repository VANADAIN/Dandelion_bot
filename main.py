import config
from aiogram import Bot, Dispatcher, executor, types

COMMANDS_LIST = {
    '!start' : 'Start bot',
    '!help' : 'Show available commands' 
    }

# Initialize bot and dispatcher
bot = Bot(token = config.API_TOKEN)
dp = Dispatcher(bot)

# --- Можно сделать все комманды в отдельном файле ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi !\nI'm Dandelion_bot !")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    response = ""
    for command, description in COMMANDS_LIST.items():
        line = command + "  -  " + description + "\n " 
        response += line
    await message.answer(f'Available commands: \n\n {response}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True) 
