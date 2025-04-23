from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.my_services_keyboard import my_services_menu
from .start import process_start 

router = Router()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await process_start(callback.from_user.id, callback.from_user.username, callback.message)
    await callback.answer()

    
# @router.callback_query(F.data.in_({"buy_proxy", "back_proxy"}))
# async def show_buy_proxy(callback: CallbackQuery):
#     await proxy_screen(callback)
    

@router.callback_query(F.data == "my_services")
async def my_services_screen(callback: CallbackQuery):
    photo = FSInputFile("bot/media/telegram.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption=(''),
        reply_markup=my_services_menu
    )
    await callback.answer()