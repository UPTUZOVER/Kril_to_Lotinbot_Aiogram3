from aiogram import Bot, Dispatcher, types, F
import asyncio
from anaylise import *
from baza import *
import os
import time
from read_word import *


token = "6871114067:AAHrDHSIkgPSXBi8vlfPoRLx_MBpUBDPrXQ"

bot = Bot(token=token)
dp = Dispatcher()

from aiogram.filters import CommandStart


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Salom alaykum bratim bu bot kril tiligadi matn yoki lotin tiliga utkazib beradi Yoki lotinni krilga utkazib beradi faaqat sukinma KALLANI ISHLAT')


@dp.message(F.text)
async def test(message: types.Message):
    text = message.text
    if has_cyrillic(text=text):
        await message.answer(to_latin(text))
    else:
        await message.answer(to_cyrillic(text))

@dp.message(F.document)
async def document(message: types.Message):
    document = message.document
    file_name = str(document.file_name)
    file_size = document.file_size
    file_id = document.file_id
    file_type = str(document.mime_type)
    document_type = file_name[file_name.rindex(".")+1:]
    if document_type == "txt" or document_type == "docx":

        custom_name = f"{message.from_user.id}_{time.time()}.docx"
        file = await bot.get_file(file_id=file_id)
        await bot.download(file=file, destination=custom_name)
        import asyncio

        green = "🟩"
        white = "⬜"
        data = await message.answer("file received")
        await asyncio.sleep(2)
        for i in range(1, 11):
            await data.edit_text(f'file uploading to server...\n' f"{i * green}{(10 - i) * white}")
            await asyncio.sleep(0.5)  # Adjust the duration as needed (0.5 seconds for each iteration)
        await asyncio.sleep(2)  # Wait for 5 seconds
        await data.delete()
        word_reader(file=custom_name)
        new_document = types.input_file.FSInputFile(path=f'{custom_name}', filename=file_name)
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_document')
        await message.answer_document(document=new_document)
        try:
            if os.path.isfile(custom_name):
                os.remove(custom_name)
        except:
            pass

    else:
        await message.answer("word fayl tashla yani (.docx) ")

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main=main())

"""
from aiogram import types, Dispatcher, Bot, F
import asyncio
from anaylise import has_cyrillic
from baza import to_cyrillic, to_latin
from read_word import word_reader
import os

token = '6871114067:AAHrDHSIkgPSXBi8vlfPoRLx_MBpUBDPrXQ'
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(F.text)
async def get_message(message: types.Message):
    text = message.text
    if has_cyrillic(text=text):
        await message.answer(to_latin(text))
    else:
        await message.answer(to_cyrillic(text))


@dp.message(F.document)
async def get_document(message: types.Message):
    document = message.document
    file_name = str(document.file_name)
    file_size = document.file_size
    file_id = document.file_id
    file_type = str(document.mime_type)
    document_type = file_name[file_name.rindex('.') + 1:]
    if document_type == 'docx':
        import time
        custom_name = f"{message.from_user.id}_{time.time()}.docx"
        file = await bot.get_file(file_id=file_id)
        await bot.download(file=file, destination=custom_name)
        green = '🟩'
        white = '⬜️'
        data = await message.answer("Fayl qabul qilindi")
        for i in range(1, 11):
            await data.edit_text(f"Fayl serverga yuklanmoqda...\n" \
                                 f"{i * green}{(10 - i) * white}")
        await data.delete()
        word_reader(file=custom_name)
        new_document = types.input_file.FSInputFile(path=custom_name, filename=file_name)
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_document')
        await message.answer_document(document=new_document, caption="Rahmat botdan foydalanganiz uchun!")
        try:
            if os.path.isfile(custom_name):
                os.remove(custom_name)
        except:
            pass

    else:
        await message.answer("Iltimos Word(.docx) tipidagi fayl tashang!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())"""