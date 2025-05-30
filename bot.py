import logging


from aiogram.utils.executor import start_polling
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import Database






TOKEN = ''
logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(token=TOKEN)
disp = Dispatcher(bot, storage=memory)
db = Database("db")
CHANNEL_ID = "@AnonymousBotRu"

def chek_sub(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


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
        if chek_sub(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
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

        else:
            await bot.send_message(message.from_user.id, "Вы не подписаны на канал.\nПодпишитесь на канал чтобы пользоваться ботом\nСсылка: https://t.me/AnonymousBotRu")
        

@disp.message_handler(content_types="photo")
async def sendPhoto(pic):
    chat_info = db.get_active_chat(pic.from_user.id)
    try:
        await bot.send_photo(chat_info[1], pic.photo[-1].file_id)
    except:
        await bot.send_message(pic.from_user.id, "Вы сейчас не в диалоге")





#992892571 мой айди тг 
#aiogram==2.22.1

if __name__ == '__main__':
    start_polling(disp, skip_updates=True)
