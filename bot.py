import logging

from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import Database


TOKEN = '2135375539:AAFh_iqlCXVCWQ5z_FpsL8av1uObE2ytOoU'
WEBHOOK_HOST = 'https://telegram-anonymous-bot.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 5000




logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(token=TOKEN)
disp = Dispatcher(bot, storage=memory)
disp.middleware.setup(LoggingMiddleware())
db = Database("db")

class FSM(StatesGroup):
    gender = State()


@disp.message_handler(commands= 'start')
async def start(message: types.Message):
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("М")
    item2 = types.KeyboardButton("Ж")
    keyboard1.add(item1)
    keyboard1.add(item2)

    
    await FSM.gender.set()
    await bot.send_message(message.from_user.id, "Привет! Я анонимный телеграмм бот, для начала укажи свой пол", reply_markup=keyboard1)


@disp.message_handler(state=FSM.gender)
async def gender(message: types.Message, state: FSMContext):
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👥Поиск собеседника")
    keyboard2.add(item1)
    async with state.proxy() as data:
        data["gender"] = message.text
        db.get_info(message.from_user.id, message.from_user.first_name, data["gender"])
    await bot.send_message(message.from_user.id, "Отлично! Теперь можно начинать", reply_markup=keyboard2)

    await state.finish()

@disp.message_handler(commands="stop")
async def stop(message: types.Message):
    info_chat = db.get_active_chat(message.from_user.id)
    if info_chat != False:
        db.delete_chat(info_chat[0])
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("👥Поиск собеседника")
        keyboard1.add(item1)

        await bot.send_message(message.from_user.id, "Вы вышли из чата", reply_markup=keyboard1)
        await bot.send_message(info_chat[1], "Собеседник покинул чат", reply_markup=keyboard1)
    else:
        await bot.send_message(message.from_user.id, "Вы не начали чат", reply_markup=keyboard1)


@disp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == "private":
        if message.text == "👥Поиск собеседника":
            keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("❌Остановить поиск")
            keyboard1.add(item1)

            chat_2 = db.get_user_id()

            if db.create_chat(message.from_user.id, chat_2) == False:
                db.add_waiting(message.from_user.id)
                await bot.send_message(message.from_user.id, "🌀Идёт поиск", reply_markup=keyboard1)

            else:
                keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("/stop")
                keyboard1.add(item1)

                await bot.send_message(message.from_user.id, "Собеседник найден! Чтобы остановить диалог, нажмите /stop", reply_markup=keyboard1)
                await bot.send_message(chat_2, "Собеседник найден! Чтобы остановить диалог, нажмите /stop", reply_markup=keyboard1)


        elif message.text == "❌Остановить поиск":
            db.delete_wating(message.from_user.id)
            keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("👥Поиск собеседника")
            keyboard1.add(item1)

            await bot.send_message(message.from_user.id, "❌Поиск остановлен", reply_markup=keyboard1)
            
        else:
            chat_info = db.get_active_chat(message.from_user.id)
            try:
                await bot.send_message(chat_info[1], message.text)
            except:
                await bot.send_message(message.from_user.id, "Вы сейчас не в диалоге")


async def on_startup(disp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(disp):
    logging.warning('shutting down...')

    await bot.delete_webhook()

    # await disp.storage.close()
    # await disp.storage.wait_closed()

    logging.warning('Bye!')


#992892571 мой айди тг 
#aiogram==2.22.1

if __name__ == '__main__':
    start_webhook(
        dispatcher=disp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
