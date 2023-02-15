import asyncio
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import Bot, Router, F
from services.services import my_password_generate
from services.services import password_policy_checked
from config_data.config import Config, load_config
from keyboards.keyboards import *
from handlers.filter import MyCallback


configg: Config = load_config()

bot: Bot = Bot(token=configg.tg_bot.token, parse_mode='HTML')
router: Router = Router()


@router.message(CommandStart())
async def process_start_message(message: Message):
    await message.answer(text=LEXICON_RU[message.text])
    await message.answer(text=LEXICON_RU['menu'], reply_markup=kb_start.as_markup(row_width=1))


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU[message.text])


@router.callback_query(MyCallback.filter(F.a == 'menu'))
async def process_button_menu(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['menu'], reply_markup=kb_start.as_markup(row_width=1))


@router.callback_query(MyCallback.filter(F.a == 'generate_password'))
async def process_generate_button(callback: CallbackQuery):
    password = my_password_generate()
    await callback.message.answer(text=LEXICON_RU['made_password'] + f'<code>{password}</code>',
                                  reply_markup=kb_generate.as_markup(row_width=1), parse_mode='HTML')


@router.callback_query(MyCallback.filter(F.a == 'another_password'))
async def process_more_password(callback: CallbackQuery):
    password = my_password_generate()
    await callback.message.answer(text=LEXICON_RU['made_password'] + f'<code>{password}</code>',
                                  reply_markup=kb_generate.as_markup(row_width=1), parse_mode='HTML')


@router.callback_query(MyCallback.filter(F.a == 'check_password'))
async def process_check_password(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['send_password'],
                                     reply_markup=kb_check_password.as_markup(row_width=1))


@router.message(Text)
async def process_got_password(message: Message):
    await message.answer(password_policy_checked(message.text),
                         reply_markup=kb_checked_password.as_markup(row_width=1))


@router.callback_query(MyCallback.filter(F.a == 'give_advices'))
async def process_give_advices(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message1'],
                                  reply_markup=kb_give_advices.as_markup(row_width=1))


@router.callback_query(MyCallback.filter(F.a == 'next_advice1'))
async def process_next_advice1(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message2'], reply_markup=kb_give_advice2.as_markup())


@router.callback_query(MyCallback.filter(F.a == 'next_advice2'))
async def process_next_advice2(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message3'], reply_markup=kb_give_advice3.as_markup())


@router.callback_query(MyCallback.filter(F.a == 'next_advice3'))
async def process_next_advice3(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message4'], reply_markup=kb_give_advice4.as_markup())


@router.callback_query(MyCallback.filter(F.a == 'next_advice4'))
async def process_next_advice4(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message5'], reply_markup=kb_give_advice5.as_markup())


@router.callback_query(MyCallback.filter(F.a == 'next_advice5'))
async def process_bonus_advice(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['advices_message6'], reply_markup=kb_before_comic.as_markup())


@router.callback_query(MyCallback.filter(F.a == 'bonus_message'))
async def process_comic(callback: CallbackQuery):
    comic = "https://linux-faq.ru/thumb.php?src=e_MEDIA_IMAGE/2016-02/password_strength.jpg&w=400"
    await callback.message.answer_photo(photo=comic)
    await callback.message.answer(text=LEXICON_RU['advices_message7'],
                                  reply_markup=kb_advices_end.as_markup(row_width=1))


@router.message()
async def other_message(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])
