
import settings
import time
import asyncio
import threading
import schedule
import os
from os.path import join, dirname
from dotenv import load_dotenv
from scheduler import Scheduler
from notifier import Notifier
from aiogram import Bot, Dispatcher, executor, types

COMMANDS_LIST = {
    '!start': 'Start bot',
    '!help': 'Show available commands',
    '!schedule': 'Create schedule',
    '!shedule_day': "Create a day note for your schedule"
}

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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
async def welcome_schedule(message: types.Message):

    ScheduleWelcomeMessage = "Fill the schedule with this schema :\n\nSchedule Name\n\nDay of the week\nItem_1-begin_time-end_time\nItem_2...\n\nWrite time like this: 14:00. There you create schema for 1 day only!"
    await message.answer(ScheduleWelcomeMessage)

    @dp.message_handler(lambda message: message.text and message.text.lower() != "")
    async def create_shedule_day(message: types.Message):

        sdlr = Scheduler(message.text)
        user_id = sdlr.get_user_id(message.chat.id)

        dictionary = sdlr.set_schedule_day()  # get day dict
        await sdlr.write_schedule_day(day_info=dictionary, id=user_id)


@dp.message_handler(commands=['notif_switch'])
async def manage_notifier(message: types.Message):
    notif = Notifier()
    msg = notif.switch_activity()
    await message.answer(msg)


async def send():
    n = Notifier()
    print("working 111...")
    msg = n.send_notification()
    print("working 222...")
    print(f"msg ::: {msg}")
    if msg == False:
        pass
    else:
        print('TO TELEGRAM')
        print(f'sending to id={msg[0]} with text: {msg[1]} ')
        await bot.send_message(chat_id=int(msg[0]), text=msg[1])


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(60, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(60, repeat, send, loop)
    executor.start_polling(dp, skip_updates=settings.SKIP_UPDATE_STATUS)
