
import config
import time
import threading
from scheduler import Scheduler
from notifier import Notifier
from aiogram import Bot, Dispatcher, executor, types

COMMANDS_LIST = {
    '!start': 'Start bot',
    '!help': 'Show available commands',
    '!schedule': 'Create schedule',
    '!shedule_day': "Create a day note for your schedule"
}

bot = Bot(token=config.API_TOKEN)
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
        user_id = sdlr.get_user_id(message.from_user.id)

        dictionary = sdlr.set_schedule_day()  # get day dict
        await sdlr.write_schedule_day(day_info=dictionary, id=user_id)


@dp.message_handler(commands=['notif_switch'])
async def manage_notifier(message: types.Message):
    notif = Notifier()
    msg = notif.switch_activity()
    await message.answer(msg)


def send():
    n = Notifier()
    while True:
        time.sleep(60)
        msg = n.send_notification()
        print("working...")
        if msg == False:
            pass
        else:
            bot.send_message(chat_id=msg[0], text=msg[1])


def main():
    t = threading.Thread(target=send, name="тест")
    t.start()
    executor.start_polling(dp, skip_updates=config.SKIP_UPDATE_STATUS)


if __name__ == '__main__':
    main()
